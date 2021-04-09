package com.cge.cgeenergy

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.ActualDateAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Actual_response_date
import kotlinx.android.synthetic.main.activity_table.*


class TableActivity : AppCompatActivity() {


    private lateinit var actualDateResponseList: List<Actual_response_date>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        actualDateResponseList = DataManager.actualDateResponse
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = actualDateResponseList[0].areaName+" ("+actualDateResponseList[0].mapCode +") "
        titleText.text=DataManager.selectedTable
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Actual_response_date()
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
        titleobject.actualTotalLoadValue = "ACTUAL TOTAL LOAD VALUE"
        titleobject.updateTimeUTC= "UPDATE TIME UTC"


        (actualDateResponseList as MutableList).add(0, titleobject)

        var viewAdapter = ActualDateAdapter(actualDateResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

