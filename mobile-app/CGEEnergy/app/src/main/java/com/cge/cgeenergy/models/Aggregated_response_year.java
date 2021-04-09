package com.cge.cgeenergy.models;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
public class Aggregated_response_year {

        @SerializedName("ActualGenerationOutputByMonthValue")
        @Expose
        private String actualGenerationOutputByMonthValue;
        @SerializedName("AreaName")
        @Expose
        private String areaName;
        @SerializedName("AreaTypeCode")
        @Expose
        private String areaTypeCode;
        @SerializedName("Dataset")
        @Expose
        private String dataset;
        @SerializedName("MapCode")
        @Expose
        private String mapCode;
        @SerializedName("Month")
        @Expose
        private String month;
        @SerializedName("ProductionType")
        @Expose
        private String productionType;
        @SerializedName("ResolutionCode")
        @Expose
        private String resolutionCode;
        @SerializedName("Source")
        @Expose
        private String source;
        @SerializedName("Year")
        @Expose
        private String year;

        public String getActualGenerationOutputByMonthValue() {
            return actualGenerationOutputByMonthValue;
        }

        public void setActualGenerationOutputByMonthValue(String actualGenerationOutputByMonthValue) {
            this.actualGenerationOutputByMonthValue = actualGenerationOutputByMonthValue;
        }

        public String getAreaName() {
            return areaName;
        }

        public void setAreaName(String areaName) {
            this.areaName = areaName;
        }

        public String getAreaTypeCode() {
            return areaTypeCode;
        }

        public void setAreaTypeCode(String areaTypeCode) {
            this.areaTypeCode = areaTypeCode;
        }

        public String getDataset() {
            return dataset;
        }

        public void setDataset(String dataset) {
            this.dataset = dataset;
        }

        public String getMapCode() {
            return mapCode;
        }

        public void setMapCode(String mapCode) {
            this.mapCode = mapCode;
        }

        public String getMonth() {
            return month;
        }

        public void setMonth(String month) {
            this.month = month;
        }

        public String getProductionType() {
            return productionType;
        }

        public void setProductionType(String productionType) {
            this.productionType = productionType;
        }

        public String getResolutionCode() {
            return resolutionCode;
        }

        public void setResolutionCode(String resolutionCode) {
            this.resolutionCode = resolutionCode;
        }

        public String getSource() {
            return source;
        }

        public void setSource(String source) {
            this.source = source;
        }

        public String getYear() {
            return year;
        }

        public void setYear(String year) {
            this.year = year;
        }

    }