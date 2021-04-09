package com.cge.cgeenergy

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.DayMonthAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Day_response_month
import kotlinx.android.synthetic.main.activity_table.*


class DayMonthActivity : AppCompatActivity() {


    private lateinit var dayMonthResponseList: List<Day_response_month>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        dayMonthResponseList = DataManager.dayMonthResponse

        titleText.text=DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = dayMonthResponseList[0].areaName+" ("+dayMonthResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Day_response_month()
        titleobject.source= "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode= "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.day = "DAY"
        titleobject.dayAheadTotalLoadForecastByDayValue = "DAY AHEAD TOTAL LOAD FORECAST VALUE"


        (dayMonthResponseList as MutableList).add(0, titleobject)

        var viewAdapter = DayMonthAdapter(dayMonthResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

