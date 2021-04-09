package com.cge.cgeenergy

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.AggregatedDateAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.Aggregated_response_date
import kotlinx.android.synthetic.main.activity_table.*


class AggregatedDateActivity : AppCompatActivity() {


    private lateinit var aggregatedDateResponseList: List<Aggregated_response_date>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_table)

        aggregatedDateResponseList = DataManager.aggregatedDateResponse

        titleText.text=DataManager.selectedTable
        val at = findViewById<TextView>(R.id.areaname_text)
        at.text = aggregatedDateResponseList[0].areaName+" ("+aggregatedDateResponseList[0].mapCode +") "
        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = Aggregated_response_date()
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
        titleobject.productionType = "PRODUCTION TYPE"
        titleobject.actualGenerationOutputValue = "ACTUAL GENERATION OUTPUT VALUE"
        titleobject.updateTimeUTC= "UPDATE TIME UTC"


        (aggregatedDateResponseList as MutableList).add(0, titleobject)

        var viewAdapter = AggregatedDateAdapter(aggregatedDateResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }
}
