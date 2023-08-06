//
// Created by jorge on 12/16/20.
//

#ifndef FTDCPARSER_DATASET_H
#define FTDCPARSER_DATASET_H

#include <string>
#include <vector>
#include <map>
#include <mutex>

#include "SampleLocation.h"
#include "Chunk.h"
#include "FileParsedData.h"
#include "Timestamp.h"
#include "Metrics.h"
#include "MetricsToWTMap.h"


class Dataset {

public:
    Dataset() : samplesInDataset(0),  metricNames(0), lazyParsing(0) {};
    Dataset(std::string csvFileName);

    void addChunk(Chunk *pChunk);
    size_t getChunkCount() { return chunkVector.size(); }
    Chunk *getChunk(size_t n) { return (n < chunkVector.size()) ? chunkVector[n] : nullptr; }
    std::vector<Chunk *> getChunkVector() { return chunkVector; }
    // TODO: merge to have only one signature
    size_t getMetricsNames(std::vector< std::string> & metricNames);
    std::vector<std::string> getMetricsNames();

    MetricsPtr getMetric(std::string   metricName, Timestamp start=Chunk::INVALID_TIMESTAMP_POS, Timestamp end=Chunk::INVALID_TIMESTAMP_POS, bool ratedMetric=false);
    uint64_t getMetricValue(std::string metricName, size_t pos);

    size_t getMetricNamesCount() { return metricNames.size(); }
    void sortChunks();
    void finishedParsingFile(std::string path, uint64_t start, uint64_t end, size_t samplesInFile);
    bool IsMetricInDataset(const std::string& metric);
    std::vector<FileParsedData*> getParsedFileInfo() {  return this->filesParsed; }
    size_t LoadMetricsNamesFromChunk();
    void setLazyParsingFlag(bool lazy) { lazyParsing = lazy; }
    bool getLazyParsing() const { return lazyParsing; }
    std::vector<MetricsPtr> getMetrics( std::vector<std::string> metricNames,
                                                 size_t start,  size_t end,
                                                 bool ratedMetrics);
    MetricsPtr getMetricMatrix( std::vector<std::string> metricNames, size_t *stride, Timestamp start,  Timestamp end,
                     bool ratedMetrics);
    Timestamp getStartTimestamp();
    Timestamp getEndTimestamp();
    std::string getJsonFromTimestamp(Timestamp ts);
    std::string getCsvFromTimestamp(Timestamp ts);
    std::string getJsonAtPosition(int pos);
    SampleLocation getLocationInMetric(Timestamp ts, bool fromStart);
    int releaseChunks();
    void SetMetadata(std::string metadata);
    std::string getMetadata() { return metadata; }

private:
    std::vector<FileParsedData *> filesParsed;
    MetricsPtr assembleMetricFromChunks(std::string name,  SampleLocation startLocation, SampleLocation endLocation);
    bool ConvertToRatedMetric(MetricsPtr pVector);


private:
    std::vector<Chunk*> chunkVector;
    size_t samplesInDataset;
    std::mutex mu;
    std::vector<std::string> metricNames;
    std::string metadata;

    bool lazyParsing;


};



#endif //FTDCPARSER_DATASET_H
