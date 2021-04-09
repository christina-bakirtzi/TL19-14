package com.cge.cgeenergy

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.AggregatedYearAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Aggregated_response_year
import kotlinx.android.synthetic.main.activity_table.*

class AggregatedYearActivity : AppCompatActivity() {


    private lateinit var aggregatedYearResponseList: List<Aggregated_response_year>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        aggregatedYearResponseList = DataManager.aggregatedYearResponse

        titleText.text = DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = aggregatedYearResponseList[0].areaName+" ("+aggregatedYearResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Aggregated_response_year()
        titleobject.source= "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode= "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.productionType = "PRODUCTION TYPE"
        titleobject.actualGenerationOutputByMonthValue= "ACTUAL GENERATION OUTPUT VALUE"


        (aggregatedYearResponseList as MutableList).add(0, titleobject)

        var viewAdapter = AggregatedYearAdapter(aggregatedYearResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}

