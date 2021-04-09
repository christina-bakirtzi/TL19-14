package com.cge.cgeenergy

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.AggregatedMonthAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Aggregated_response_month
import kotlinx.android.synthetic.main.activity_table.*


class AggregatedMonthActivity : AppCompatActivity() {


    private lateinit var aggregatedMonthResponseList: List<Aggregated_response_month>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        aggregatedMonthResponseList = DataManager.aggregatedMonthResponse

        titleText.text=DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = aggregatedMonthResponseList[0].areaName+" ("+aggregatedMonthResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Aggregated_response_month()
        titleobject.source= "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode= "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.day = "DAY"
        titleobject.productionType = "PRODUCTION TYPE"
        titleobject.actualGenerationOutputByDayValue= "ACTUAL GENERATION OUTPUT VALUE"


        (aggregatedMonthResponseList as MutableList).add(0, titleobject)

        var viewAdapter = AggregatedMonthAdapter(aggregatedMonthResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

