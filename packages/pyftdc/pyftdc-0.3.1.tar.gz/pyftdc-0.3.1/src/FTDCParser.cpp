//
// Created by jorge on 11/2/20.
//
#include <FTDCParser.h>
#include <ParserTasksList.h>
#include <sys/stat.h>
#include <string>

// From libbson
#include <bson/bson.h>

#include <sys/resource.h>

#include "JSONWriter.h"
#include "CSVWriter.h"
#include "spdlog/sinks/basic_file_sink.h"

#include <spdlog/spdlog.h>
#include <dirent.h>


static double double_time_of_day() {
    struct timeval timeval{};
    bson_gettimeofday(&timeval);
    return (timeval.tv_sec + timeval.tv_usec * 0.000001);
}


std::string
FTDCParser::parseInfoChunk(const bson_t *bson) {

    size_t length=0;
    auto json = bson_as_json(bson, &length);
    //metadata.emplace_back(json);
    std::string ret =  std::string (json);
    bson_free(json);
    return ret;
}


bson_reader_t *
FTDCParser::open(std::string file_path) {

    bson_error_t error;

    // File exists?
    struct stat data{};
    if (stat(file_path.c_str(), &data) != 0) {
        spdlog::error("Failed to find file '{}'", file_path  );
        return nullptr;
    }

    // Initialize a new reader for this file descriptor.
    bson_reader_t *reader;
    if (!(reader = bson_reader_new_from_file(file_path.c_str(), &error))) {
        spdlog::error( "Failed to open file '{}'", file_path  );
        return nullptr;
    }
    return reader;
}

std::vector<Dataset *>
FTDCParser::parseFiles(std::vector<std::string> files, bool onlyMetadata, bool onlyMetricNames, bool lazyParsing) {

    std::vector<Dataset *> dataSets = *new std::vector<Dataset*>;

    for (auto file : files) {
        auto ds = parseFile(file, onlyMetadata, onlyMetricNames, lazyParsing );
        dataSets.emplace_back(ds);
    }
    return dataSets;
}


std::vector<Dataset *>
FTDCParser::parseDir(std::string path, bool onlyMetadata, bool onlyMetricNames, bool lazyParsing) {

    std::vector<Dataset *> dataSets = *new std::vector<Dataset*>;
    struct stat buffer{0};

    if (stat(path.c_str(), &buffer) == 0
         && (buffer.st_mode & S_IFMT) == S_IFDIR) {
        std::vector<std::string> fileNames;

        auto dp = opendir(path.c_str());
        if (dp!= nullptr) {
            dirent *entry = nullptr;
            while ((entry = readdir(dp))) {
                struct stat file_stats{0};
                if ( (stat(entry->d_name, &file_stats) == 0) && ((file_stats.st_mode & S_IFMT) != S_IFDIR))
                   fileNames.emplace_back(entry->d_name);
            }
        }
        return parseFiles(fileNames, onlyMetadata, onlyMetricNames, lazyParsing);
    }

    return std::vector<Dataset *>();
}

Dataset *
FTDCParser::parseFile(std::string fileName,
                       const bool onlyMetadata,
                       const bool onlyMetricNames,
                       const bool lazyParsing) {
    bson_reader_t *reader;
    const bson_t *pBsonChunk;
    double date_time_before, date_time_after, date_time_delta;

    ParserTasksList parserTaskList;

    Dataset *dataSet = new Dataset();

    dataSet->setLazyParsingFlag(lazyParsing);

    spdlog::debug( "File: {}", fileName);
    reader = this->open(fileName);
    if (!reader) return nullptr;

    date_time_before = double_time_of_day();

    bool at_EOF = false;
    unsigned int chunkCount = 0;
    bool parsing_values = false;
    uint64_t first_id = INVALID_TIMESTAMP;
    uint64_t current_id = INVALID_TIMESTAMP;

    while ((pBsonChunk = bson_reader_read(reader, &at_EOF))) {

        spdlog::debug( "Chunk # {} length: {}", chunkCount , pBsonChunk->len);
        if (!parsing_values) {
            dataSet->SetMetadata(parseInfoChunk(pBsonChunk));
            parsing_values = true;
            if (onlyMetadata and !onlyMetricNames) break;
        } else {
            bson_iter_t iter;

            if (bson_iter_init(&iter, pBsonChunk)) {
                while (bson_iter_next(&iter)) {

                    if (BSON_ITER_HOLDS_BINARY(&iter)) {
                        bson_subtype_t subtype;
                        uint32_t bin_size;
                        const uint8_t *data;
                        bson_iter_binary(&iter, &subtype, &bin_size, reinterpret_cast<const uint8_t **>(&data));

                        // the memory pointed to by data is managed internally. Better make a copy
                        uint8_t *bin_data = new uint8_t[bin_size];
                        memcpy(bin_data, data, bin_size);
                        spdlog::debug("Parser task: size={}  Id={}",  bin_size, current_id);

                        // Add to the list chunks to be decompressed and parsed.
                        parserTaskList.push(bin_data, bin_size, current_id);

                    } else if (BSON_ITER_HOLDS_DATE_TIME(&iter)) {

                        current_id = bson_iter_date_time(&iter);
                        if (first_id == INVALID_TIMESTAMP) first_id = current_id;
                    } else if (BSON_ITER_HOLDS_INT32(&iter)) { ; // type = bson_iter_int32(&iter);
                    }
                }
            }

            if (onlyMetricNames || onlyMetadata)
                break;
        }
        ++chunkCount;
    }

    parserTaskList.parseTasksParallel(dataSet);

    if (!at_EOF)
        spdlog::error("Not all chunks were parsed.") ;

    date_time_after = double_time_of_day();
    date_time_delta = BSON_MAX ((double) (date_time_after - date_time_before), 0.000001);

    // This is the end of a file being parsed.
    dataSet->finishedParsingFile(fileName, first_id, current_id, chunkCount);

    spdlog::info("File parsed in {} seconds. There are {} chunks, {} metrics.",
                 date_time_delta, dataSet->getChunkCount(),dataSet->getMetricNamesCount() );
    struct rusage usage{0};
    getrusage(RUSAGE_SELF, &usage);

    spdlog::info("maximum resident set size: {}. Integral shared memorysize: {}. Integral unshared data size: {}. Integral unshared stack size: {}",
                 usage.ru_maxrss, usage.ru_ixrss, usage.ru_idrss, usage.ru_isrss);

    if (onlyMetricNames) {
        std::vector<std::string> names;
        dataSet->getMetricsNames(names);
        int i=0;
        for (auto name : names ) {
            spdlog::debug("({}/{}): {}", i, names.size(), name);
        }
    }

    // Cleanup after our reader, which closes the file descriptor.
    bson_reader_destroy(reader);

    return dataSet;
}

std::vector<std::string>
FTDCParser::getMetricsNamesPrefixed(std::string prefix, Dataset *ds) {
    std::vector<std::string> names;

    std::vector<std::string> metricNames;
    ds->getMetricsNames(metricNames);

    for (auto & m : metricNames) {
        if (prefix == m.substr(0, prefix.size()))
            names.push_back(m);
    }
    return names;
}

std::vector<std::string>
FTDCParser::getMetricsNames(Dataset *ds) {
    std::vector<std::string> metricNames;
    ds->getMetricsNames(metricNames);
    return metricNames;
}

size_t
FTDCParser::dumpDocsAsJsonTimestamps(const std::string  inputFile, const std::string  outputFile,
                                     const Timestamp start, const Timestamp end) {

    auto dataSet = parseFile(inputFile, false, false, false);
    if (dataSet) {

        JSONWriter w;
        return  w.dumpTimestamps( dataSet, outputFile, start, end, false);
    }
    else
        return 0;
}


size_t
FTDCParser::dumpDocsAsCsvTimestamps(std::string inputFile, std::string outputFile, Timestamp start, Timestamp end) {

    auto dataSet = parseFile(inputFile, false, false, false);
    if (!dataSet) {

        CSVWriter c;
        c.dumpCSVTimestamps(dataSet, outputFile, start, end, false);
        return 1;
    }
    else
        return 0;
}

void FTDCParser::setVerbose(bool verbosity) {

        if (verbose)
            spdlog::set_level(spdlog::level::debug);
        else
            spdlog::set_level(spdlog::level::info);

        verbose = verbosity;
}

FTDCParser::FTDCParser() {
    ;  // logger = spdlog::basic_logger_mt("parser_logger", "parser.log");
}

