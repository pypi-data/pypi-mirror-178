//
// Created by jorge on 11/2/20.
//

#ifndef FTDCPARSER_FTDCPARSER_H
#define FTDCPARSER_FTDCPARSER_H

#include <Chunk.h>
#include <Dataset.h>

#include <string_view>
#include <string>

// From libbson
#include <bson/bson.h>
#include "spdlog/logger.h"

class FTDCParser    {
public:
    FTDCParser();

    bson_reader_t* open(std::string file_path);

    std::vector<Dataset *>  parseFiles(std::vector<std::string> files, bool onlyMetadata=false, bool onlyMetricNames=false, bool lazyParsing=false) ;
    std::vector<Dataset *>  parseDir(std::string path, bool onlyMetadata= false, bool onlyMetricNames= false, bool lazyParsing= false) ;
    Dataset * parseFile(std::string file, bool onlyMetadata=false, bool onlyMetricNames=false, bool lazyParsing=false);

    std::string parseInfoChunk (const bson_t *bson);
    std::vector<std::string> getMetricsNamesPrefixed(std::string prefix, Dataset *ds) ;
    std::vector<std::string> getMetricsNames(Dataset *ds);
    //std::vector<std::string> getMetadata() { return metadata; }

    size_t dumpDocsAsJsonTimestamps( std::string  inputFile,  std::string  outputFile, Timestamp start, Timestamp end);
    size_t dumpDocsAsCsvTimestamps( std::string  inputFile,  std::string  outputFile, Timestamp start, Timestamp end);

    std::string getJsonAtPosition(size_t position);

    void setVerbose(bool verbosity);

private:
    std::shared_ptr<spdlog::logger> logger;
    bool verbose = false;
};


#endif //FTDCPARSER_FTDCPARSER_H