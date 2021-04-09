package com.cge.cgeenergy


import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.DayYearAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Day_response_year
import kotlinx.android.synthetic.main.activity_table.*

class DayYearActivity : AppCompatActivity() {


    private lateinit var dayYearResponseList: List<Day_response_year>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        dayYearResponseList = DataManager.dayYearResponse

        titleText.text = DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = dayYearResponseList[0].areaName+" ("+dayYearResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Day_response_year()
        titleobject.source= "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode= "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.dayAheadTotalLoadForecastByMonthValue = "DAY AHEAD TOTAL LOAD FORECAST VALUE"



        (dayYearResponseList as MutableList).add(0, titleobject)

        var viewAdapter = DayYearAdapter(dayYearResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

