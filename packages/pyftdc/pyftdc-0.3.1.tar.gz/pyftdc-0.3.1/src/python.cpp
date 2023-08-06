#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "FTDCParser.h"
#include <vector>
#include <filesystem>


namespace py = pybind11;

using namespace py::literals;
using namespace ftdcparser;
namespace fs = std::filesystem;

typedef std::vector<std::string> MetricNames;


#define FALSE 0

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

//TODO: Check for memory leaks.



// helper function to avoid making a copy when returning a py::array_t
// author: https://github.com/YannickJadoul
// source: https://github.com/pybind/pybind11/issues/1042#issuecomment-642215028
template <typename Sequence>
inline py::array_t<typename Sequence::value_type>
as_pyarray(Sequence &&seq) {
    auto size = seq.size();
    auto data = seq.data();
    std::unique_ptr<Sequence> seq_ptr = std::make_unique<Sequence>(std::move(seq));
    auto capsule = py::capsule(seq_ptr.get(), [](void *p) { std::unique_ptr<Sequence>(reinterpret_cast<Sequence*>(p)); });
    seq_ptr.release();
    return py::array(size, data, capsule);
}

inline py::array_t<uint64_t >
as_pyarray(MetricsPtr m) {
    auto size = m->size();
    auto data = m->data();
    std::unique_ptr<MetricsPtr> seq_ptr = std::make_unique<MetricsPtr>(std::move(m));
    auto capsule = py::capsule(seq_ptr.get(),
                               [](void *p) { std::unique_ptr<Metrics>(reinterpret_cast<Metrics *>(p)); });
    seq_ptr.release();
    return py::array(size, data, capsule);
}

//-----------------------------------------------------------------------------------
// DatasetClass

struct DatasetClass {
    Dataset *dataSet;
    std::string filePath;
    std::string file;
    std::string metadata;
    MetricNames metricsNames;
    bool interim;
    std::vector<MetricsPtr> dataSetMetrics;

    DatasetClass() {
    }

    explicit DatasetClass(Dataset *ds, std::string path) {
        dataSet = ds;
        filePath = path;
        file = fs::path(path).filename();
        metricsNames = dataSet->getMetricsNames();
        metadata = dataSet->getMetadata();
        if (file == "metrics.interim")
            interim = true;
        else {
            interim = false;
        }
    };

    MetricsPtr
    getMetric(std::string metric_name,
                          size_t start = INVALID_TIMESTAMP, size_t end =INVALID_TIMESTAMP,
                          bool rated_metric = false) {

        auto m = dataSet->getMetric(metric_name, start, end, rated_metric);
        if (!m) {
            auto *mp = new MetricsPtr();
            return *mp;
        }
        else
            return m;
    }


    py::array_t<unsigned long>
    getMetricAsNumpyArray(std::string metric_name,
                          size_t start = INVALID_TIMESTAMP,
                          size_t end = INVALID_TIMESTAMP,
                          bool rated_metric = false) {
        auto m = getMetric(metric_name, start, end, rated_metric);

        if (m) return as_pyarray(m);
        else {
            auto  *empty = new py::array_t<unsigned long>;
            return *empty;
        }
    }

    std::vector<py::array_t<unsigned long>>
    getMetricListAsNumpyArray(std::vector<std::string> metric_names,
                              size_t start = INVALID_TIMESTAMP,
                              size_t end = INVALID_TIMESTAMP,
                              bool rated_metric = false) {

        std::vector<py::array_t<unsigned long>> metricList;
        for (auto &name : metric_names) {
            auto m = this->getMetricAsNumpyArray(name, start, end, rated_metric);
            metricList.emplace_back(m);
        }
        return metricList;
    }
};

//-----------------------------------------------------------------------------------
//

struct ParserClass {
    FTDCParser *pParser;
    Dataset *dataSet = nullptr;
    std::string metadata;
    std::vector<std::string> fileList;
    MetricNames metricNames;

    MetricsPtr emptyMetrics;

    explicit ParserClass() {
        pParser = new FTDCParser();
    };

    DatasetClass *parseFile(std::string file, bool only_metadata=false, bool only_metrics_names=false, bool lazy=false) {
        if (dataSet != nullptr) {
            delete dataSet;
            dataSet = nullptr;
        }
        dataSet = pParser->parseFile(file, only_metadata, only_metrics_names, false);
        if (dataSet) {
            // Timestamps, metric names, and metadata as fields in python
            metricNames = dataSet->getMetricsNames();
            metadata = dataSet->getMetadata();
        }
        return new DatasetClass(dataSet, file);
    }

    void setVerbose(bool verbose) {
        pParser->setVerbose(verbose);
    }

    std::vector<DatasetClass*>
    parseDir(std::string dir, bool only_metadata=false, bool only_metrics_names=false, bool lazy=false) {


        std::vector<DatasetClass*> *r = new std::vector<DatasetClass*>;
        for (const auto &entry : fs::directory_iterator(dir)) {
            if (entry.is_regular_file()) {

                //printf("******** parsing %s\n", entry.path().c_str());
                auto ds = pParser->parseFile(entry.path(),
                                             only_metadata, only_metrics_names, false);
                if (ds) {
                    DatasetClass *dsc = new DatasetClass(ds, entry.path());
                    r->emplace_back(dsc);
                }
            }
        }

        return *r;
    }

    int dumpFileAsJson(std::string input, std::string output) {
        return pParser->dumpDocsAsJsonTimestamps(input, output, INVALID_TIMESTAMP, INVALID_TIMESTAMP);
    }

    int dumpFileAsCsv(std::string input, std::string output) {
        return pParser->dumpDocsAsCsvTimestamps(input, output, INVALID_TIMESTAMP, INVALID_TIMESTAMP);
    }

    py::list
    getParsedFileInfo() {
        auto fi = dataSet->getParsedFileInfo();
        py::list parsedFiles;
        for (auto f : fi) {
            auto fileInfo = py::dict("abs_path"_a=f->getFileAbsolute(),
                                     "samples"_a=f->getSamplesCount(),
                                     "start"_a=f->getStart(),
                                     "end"_a=f->getEnd()
            );
            parsedFiles.append(fileInfo);
        }
        return parsedFiles;
    }

    MetricsPtr
    get_timestamps(size_t start =INVALID_TIMESTAMP, size_t end = INVALID_TIMESTAMP) {
        return dataSet->getMetric( "start", start, end);
    }

    MetricsPtr
    getMetric(std::string metric_name,
                          size_t start = INVALID_TIMESTAMP, size_t end =INVALID_TIMESTAMP,
                          bool rated_metric = false) {
        return dataSet->getMetric(metric_name, start, end, rated_metric);
    }

    std::vector<MetricsPtr>
    getMetricList(const std::vector<std::string> metric_names,
                                          size_t start = INVALID_TIMESTAMP,
                                          size_t end = INVALID_TIMESTAMP,
                                          bool rated_metric = false) {

        auto m = dataSet->getMetrics(metric_names, start, end, rated_metric);

        std::vector<MetricsPtr> metricList;
        for(size_t i=0;i<m.size();++i) {

            // How to handle metric names that are not found?
            if (m[i] != nullptr) {

                metricList.emplace_back(m[i]);
            }
            else
                metricList.emplace_back(emptyMetrics);
        }
        return metricList;
    }


    py::array_t<unsigned long>
    getMetricAsNumpyArray(std::string metric_name,
                          size_t start = INVALID_TIMESTAMP,
                          size_t end = INVALID_TIMESTAMP,
                          bool rated_metric = false) {
        auto m = dataSet->getMetric(metric_name, start, end, rated_metric);
        return as_pyarray(m);
    }

    std::vector<py::array_t<unsigned long>>
    getMetricListAsNumpyArray(std::vector<std::string> metric_names,
            size_t start = INVALID_TIMESTAMP,
            size_t end = INVALID_TIMESTAMP,
            bool rated_metric = false) {

        auto m = dataSet->getMetrics(metric_names, start, end, rated_metric);

        std::vector<py::array_t<unsigned long>> metricList;
        for(size_t i=0;i<m.size();++i) {

            // How to handle metric names that are not found?
            if (m[i] != nullptr) {
                auto element = as_pyarray(m[i]);
                metricList.emplace_back(element);
            }
            else {
                auto  *empty = new py::array_t<unsigned long>;
                metricList.emplace_back(*empty);
            }
        }
        return metricList;
    }

    py::array_t<uint64_t>
    getMetricListAsNumpyMatrix(const std::vector<std::string> metric_names,
                                                      size_t start = INVALID_TIMESTAMP,
                                                      size_t end = INVALID_TIMESTAMP,
                                                      bool rated_metric = false,
                                                      bool transpose = false)  {
        size_t stride = 0;
        auto m = dataSet->getMetricMatrix( metric_names, &stride, start, end, rated_metric);

        if (stride !=0) {

            int metricNamesSize = metric_names.size();
            if (!transpose) {
                return py::array_t<uint64_t>({ metricNamesSize, (int)stride}, m->data());
            }
            else {
                py::array_t<uint64_t> a = py::array_t<uint64_t>( {(int)stride, metricNamesSize});

                uint64_t   *p   = m->data();

                auto r =  a.mutable_unchecked();

                //printf("dimensions %zd x %zd\n", r.shape(0), r.shape(1));
                //printf("Element (0,0)=%ld\nElement (%ld,0)=%ld\n", p[0], r.shape(0),  p[r.shape(0)]);

                for (int i=0; i<r.shape(0); ++i) {
                    for (int j=0; j<r.shape(1); ++j)
                        r(i,j) = p[i + (j*r.shape(0))];
                }
                return a;
            }
        }
        else {
            // err
            return py::array_t<uint64_t>({ 0, 0 }, { 4, 8 });
        }
    }
};

// ------------------------------------------------------------------------
// interface

PYBIND11_MODULE(pyftdc, m) {

m.doc() = R"pbdoc(
        MongoDB FTDC files parser library.
        -----------------------

        .. currentmodule:: pyftdc

        .. autosummary::
           :toctree: _generate
    )pbdoc";

py::class_<DatasetClass>(m, "Dataset")
    .def(py::init<>())
    .def("get_metric", &DatasetClass::getMetric,
        "Returns a list of values from the metrics, using starting and ending timestamps if specified",
        py::arg("metric_name"),
        py::arg("start") = ::INVALID_TIMESTAMP,
        py::arg("end") = ::INVALID_TIMESTAMP,
        py::arg("rated_metric") = false)
    .def_readonly("interim", &DatasetClass::interim)
    .def_readonly("metadata", &DatasetClass::metadata)
    .def_readonly("metrics_names", &DatasetClass::metricsNames)
    .def_readonly("file", &DatasetClass::file)
    .def_readonly("path", &DatasetClass::filePath)
    .def_readonly("metrics", &DatasetClass::dataSetMetrics)
        .def("get_metric_numpy", &DatasetClass::getMetricAsNumpyArray,
             "Returns a metric as a numpy array.",
             py::arg("metric_name"),
             py::arg("start") = ::INVALID_TIMESTAMP,
             py::arg("end") = ::INVALID_TIMESTAMP,
             py::arg("rated_metric") = false)
        .def("get_metric_list_numpy", &DatasetClass::getMetricListAsNumpyArray,
             "Returns a list of metrics as numpy arrays.",
             py::arg("testMetricNames"),
             py::arg("start") = ::INVALID_TIMESTAMP,
             py::arg("end") = ::INVALID_TIMESTAMP,
             py::arg("rated_metric") = false);

py::class_<ParserClass>(m, "FTDCParser")
    .def(py::init<>())
    .def("set_verbose", &ParserClass::setVerbose,
         "Set verbose flag", py::arg("verbose"))
    .def("parse_dir", &ParserClass::parseDir,
        "Parses all files in a directory",
        py::arg("dir"),
        py::arg("only_metadata") = false,
        py::arg("only_metrics_names") = false,
        py::arg("lazy") = true)
    .def("parse_file", &ParserClass::parseFile,
        "Parses one file",
        py::arg("file"),
        py::arg("only_metadata") = false,
        py::arg("only_metrics_names") = false,
        py::arg("lazy") = true)
    .def("get_parsed_file_info", &ParserClass::getParsedFileInfo,
        "Returns information on parsed files")
    .def("dump_file_as_json", &ParserClass::dumpFileAsJson,
        "Dumps a file contents to a file as JSON structures.",
        py::arg("input"),
        py::arg("output"))
    .def("dump_file_as_csv", &ParserClass::dumpFileAsCsv,
        "Dumps a file contents to a file as CSV file.",
        py::arg("input"),
        py::arg("output"))

    .def("get_metric", &ParserClass::getMetric,
        "Returns a list of values from the metrics, using starting and ending timestamps if specified",
        py::arg("metric_name"),
        py::arg("start") = ::INVALID_TIMESTAMP,
        py::arg("end") = ::INVALID_TIMESTAMP,
        py::arg("rated_metric") = false)
    .def("get_metrics_list", &ParserClass::getMetricList,
        "Returns a list of values from the metrics list, using starting and ending timestamps if specified",
        py::arg("metric_name"),
        py::arg("start") = ::INVALID_TIMESTAMP,
        py::arg("end") = ::INVALID_TIMESTAMP,
        py::arg("rated_metric") = false)
    .def("get_timestamps", &ParserClass::get_timestamps,
        "Returns timestamps",
        py::arg("start") = ::INVALID_TIMESTAMP,
        py::arg("end") = ::INVALID_TIMESTAMP)
    .def_readonly("testMetricNames", &ParserClass::metricNames)
    .def_readonly("metadata", &ParserClass::metadata)
    .def("get_metric_numpy", &ParserClass::getMetricAsNumpyArray,
        "Returns a metric as a numpy array.",
        py::arg("metric_name"),
        py::arg("start") = ::INVALID_TIMESTAMP,
        py::arg("end") = ::INVALID_TIMESTAMP,
        py::arg("rated_metric") = false)
    .def("get_metrics_list_numpy", &ParserClass::getMetricListAsNumpyArray,
        "Returns a list of metrics as numpy arrays.",
        py::arg("testMetricNames"),
        py::arg("start") = ::INVALID_TIMESTAMP,
        py::arg("end") = ::INVALID_TIMESTAMP,
        py::arg("rated_metric") = false)
    .def("get_metrics_list_numpy_matrix", &ParserClass::getMetricListAsNumpyMatrix,
        "Returns a matrix of metrics.",
        py::arg("testMetricNames"),
        py::arg("start") = ::INVALID_TIMESTAMP,
        py::arg("end") = ::INVALID_TIMESTAMP,
        py::arg("rated_metric") = false,
        py::arg("transpose") = false);



#ifdef VERSION_INFO
m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
m.attr("__version__") = "dev";
#endif
} // PYBIND11_MODULE
