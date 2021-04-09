package com.cge.cgeenergy.models;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
public class Day_response_date {

        @SerializedName("AreaName")
        @Expose
        private String areaName;
        @SerializedName("AreaTypeCode")
        @Expose
        private String areaTypeCode;
        @SerializedName("Dataset")
        @Expose
        private String dataset;
        @SerializedName("DateTimeUTC")
        @Expose
        private String dateTimeUTC;
        @SerializedName("Day")
        @Expose
        private String day;
        @SerializedName("DayAheadTotalLoadForecastValue")
        @Expose
        private String dayAheadTotalLoadForecastValue;
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
        @SerializedName("UpdateTimeUTC")
        @Expose
        private String updateTimeUTC;
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

        public String getDateTimeUTC() {
            return dateTimeUTC;
        }

        public void setDateTimeUTC(String dateTimeUTC) {
            this.dateTimeUTC = dateTimeUTC;
        }

        public String getDay() {
            return day;
        }

        public void setDay(String day) {
            this.day = day;
        }

        public String getDayAheadTotalLoadForecastValue() {
            return dayAheadTotalLoadForecastValue;
        }

        public void setDayAheadTotalLoadForecastValue(String dayAheadTotalLoadForecastValue) {
            this.dayAheadTotalLoadForecastValue = dayAheadTotalLoadForecastValue;
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

        public String getUpdateTimeUTC() {
            return updateTimeUTC;
        }

        public void setUpdateTimeUTC(String updateTimeUTC) {
            this.updateTimeUTC = updateTimeUTC;
        }

        public String getYear() {
            return year;
        }

        public void setYear(String year) {
            this.year = year;
        }

    }