package com.cge.cgeenergy

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.DayDateAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Day_response_date
import kotlinx.android.synthetic.main.activity_table.*


class DayDateActivity : AppCompatActivity() {


    private lateinit var dayDateResponseList: List<Day_response_date>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        dayDateResponseList = DataManager.dayDateResponse

        titleText.text=DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = dayDateResponseList[0].areaName+" ("+dayDateResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Day_response_date()
        titleobject.source= "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode= "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.day = "DAY"
        titleobject.dateTimeUTC = "DATE TIME UTC"
        titleobject.updateTimeUTC= "UPDATE TIME UTC"
        titleobject.dayAheadTotalLoadForecastValue = "DAY AHEAD TOTAL LOAD FORECAST VALUE"


        (dayDateResponseList as MutableList).add(0, titleobject)

        var viewAdapter = DayDateAdapter(dayDateResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

