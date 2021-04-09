package com.cge.cgeenergy

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.ActualMonthAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Actual_response_month
import kotlinx.android.synthetic.main.activity_table.*


class ActualMonthActivity : AppCompatActivity() {


    private lateinit var actualMonthResponseList: List<Actual_response_month>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        actualMonthResponseList = DataManager.actualMonthResponse

        titleText.text=DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = actualMonthResponseList[0].areaName+" ("+actualMonthResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Actual_response_month()
        titleobject.source= "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode= "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.day = "DAY"
        titleobject.actualTotalLoadByDayValue = "ACTUAL TOTAL LOAD VALUE"


        (actualMonthResponseList as MutableList).add(0, titleobject)

        var viewAdapter = ActualMonthAdapter(actualMonthResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

