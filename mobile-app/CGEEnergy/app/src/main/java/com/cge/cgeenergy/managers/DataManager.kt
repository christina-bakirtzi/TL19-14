package com.cge.cgeenergy.managers

import com.cge.cgeenergy.models.*

object DataManager {

    var selectedTable: String = ""
    var actualDateResponse: List<Actual_response_date> = arrayListOf()
    var actualYearResponse: List<Actual_response_year> = arrayListOf()
    var actualMonthResponse: List<Actual_response_month> = arrayListOf()
    var aggregatedYearResponse: List<Aggregated_response_year> = arrayListOf()
    var aggregatedMonthResponse: List<Aggregated_response_month> = arrayListOf()
    var aggregatedDateResponse: List<Aggregated_response_date> = arrayListOf()
    var dayYearResponse: List<Day_response_year> = arrayListOf()
    var dayMonthResponse: List<Day_response_month> = arrayListOf()
    var dayDateResponse: List<Day_response_date> = arrayListOf()
    var avsfYearResponse: List<AvsF_response_year> = arrayListOf()
    var avsfMonthResponse: List<AvsF_response_month> = arrayListOf()
    var avsfDateResponse: List<AvsF_response_date> = arrayListOf()
}