package com.cge.cgeenergy.models;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
public class Day_response_year {

        @SerializedName("AreaName")
        @Expose
        private String areaName;
        @SerializedName("AreaTypeCode")
        @Expose
        private String areaTypeCode;
        @SerializedName("Dataset")
        @Expose
        private String dataset;
        @SerializedName("DayAheadTotalLoadForecastByMonthValue")
        @Expose
        private String dayAheadTotalLoadForecastByMonthValue;
        @SerializedName("MapCode")
        @Expose
        private String mapCode;
        @SerializedName("Month")
        @Expose
        private String month;
        @SerializedName("ResolutionCode")
        @Expose
        private String resolutionCode;
        @SerializedName("Source")
        @Expose
        private String source;
        @SerializedName("Year")
        @Expose
        private String year;

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

        public String getDayAheadTotalLoadForecastByMonthValue() {
            return dayAheadTotalLoadForecastByMonthValue;
        }

        public void setDayAheadTotalLoadForecastByMonthValue(String dayAheadTotalLoadForecastByMonthValue) {
            this.dayAheadTotalLoadForecastByMonthValue = dayAheadTotalLoadForecastByMonthValue;
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
