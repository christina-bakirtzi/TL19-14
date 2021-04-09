package com.cge.cgeenergy

import ActualYearAdapter
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Actual_response_year
import kotlinx.android.synthetic.main.activity_table.*

class ActualYearActivity : AppCompatActivity() {


    private lateinit var actualYearResponseList: List<Actual_response_year>
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        actualYearResponseList = DataManager.actualYearResponse
        titleText.text = DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = actualYearResponseList[0].areaName+" ("+actualYearResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Actual_response_year()
        titleobject.source = "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode = "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.actualTotalLoadByMonthValue = "ACTUAL TOTAL LOAD VALUE"


        (actualYearResponseList as MutableList).add(0, titleobject)

        var viewAdapter = ActualYearAdapter(actualYearResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

