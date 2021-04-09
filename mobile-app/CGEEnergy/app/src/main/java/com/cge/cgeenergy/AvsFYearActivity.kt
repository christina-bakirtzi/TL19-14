package com.cge.cgeenergy

import android.graphics.Color
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cge.cgeenergy.adapters.AvsFYearAdapter
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.models.AvsF_response_year
import com.github.mikephil.charting.charts.BarChart
import com.github.mikephil.charting.components.Legend
import com.github.mikephil.charting.components.LegendEntry
import com.github.mikephil.charting.components.XAxis
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter
import com.github.mikephil.charting.formatter.LargeValueFormatter
import kotlinx.android.synthetic.main.activity_table.*


class AvsFYearActivity : AppCompatActivity() {


    private lateinit var avsfYearResponseList: List<AvsF_response_year>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chart)



        avsfYearResponseList = DataManager.avsfYearResponse
        populateGraphData()
        titleText.text = DataManager.selectedTable
//        setUpListView()
    }

    private fun setUpListView() {
        var viewManager = LinearLayoutManager(this)

        var titleobject = AvsF_response_year()
        titleobject.source = "SOURCE"
        titleobject.dataset = "DATASET"
        titleobject.areaName = "AREA NAME"
        titleobject.areaTypeCode = "AREA CODE"
        titleobject.mapCode = "MAPCODE"
        titleobject.resolutionCode = "RESOLUTION CODE"
        titleobject.year = "YEAR"
        titleobject.month = "MONTH"
        titleobject.dayAheadTotalLoadForecastByMonthValue = "DAY AHEAD TOTAL LOAD FORECAST VALUE"
        titleobject.actualTotalLoadByMonthValue = "ACTUAL TOTAL LOAD VALUE"

        (avsfYearResponseList as MutableList).add(0, titleobject)

        var viewAdapter = AvsFYearAdapter(avsfYearResponseList)

        recyclerview.layoutManager = viewManager
        recyclerview.adapter = viewAdapter

    }

    fun populateGraphData() {

        var barChartView = findViewById<BarChart>(R.id.chartConsumptionGraph)

        val barWidth: Float
        val barSpace: Float
        val groupSpace: Float

        barWidth = 0.4f
        barSpace = 0.0f
        groupSpace = 0.2f
        var titleobject = AvsF_response_year()
        var xAxisValues = ArrayList<String>()
        var yValueGroup1 = ArrayList<BarEntry>()
        var yValueGroup2 = ArrayList<BarEntry>()
        var barDataSet1: BarDataSet
        var barDataSet2: BarDataSet
        var i=1
//        xAxisValues.add("")
        for(value in avsfYearResponseList){
            xAxisValues.add(value.month)
            yValueGroup1.add(BarEntry(i.toFloat(),value.dayAheadTotalLoadForecastByMonthValue.toFloat()))
            yValueGroup2.add(BarEntry(i.toFloat(),value.actualTotalLoadByMonthValue.toFloat()))
//            xAxisValues.add("")
            i=i+1
        }

        barDataSet1 = BarDataSet(yValueGroup1, "")
        barDataSet1.setColors(Color.CYAN, Color.CYAN)
        barDataSet1.label = "DAY AHEAD TOTAL LOAD FORECAST"
        barDataSet1.setDrawIcons(false)
        barDataSet1.setDrawValues(false)

        barDataSet2 = BarDataSet(yValueGroup2, "")
        barDataSet2.label = "ACTUAL TOTAL LOAD"
        barDataSet2.setColors(Color.BLUE, Color.BLUE)
        barDataSet2.setDrawIcons(false)
        barDataSet2.setDrawValues(false)

        var barData = BarData(barDataSet1, barDataSet2)
        barChartView.description.text = "entso-e"
        barChartView.description.isEnabled = true
        barChartView.description.textSize = 3f
        barData.setValueFormatter(LargeValueFormatter())
        barChartView.setData(barData)
        barChartView.getBarData().setBarWidth(barWidth)
        barChartView.getXAxis().setAxisMinimum(0f)
        val size = avsfYearResponseList.size.toFloat() +avsfYearResponseList.size.toFloat()
        barChartView.getXAxis().setAxisMaximum(xAxisValues.size.toFloat())
        barChartView.groupBars(0f, groupSpace, barSpace)
        barChartView.setFitBars(true)
        barChartView.getData().setHighlightEnabled(true)

        // set bar label
        var legend = barChartView.legend
        legend.setVerticalAlignment(Legend.LegendVerticalAlignment.BOTTOM)
        legend.setHorizontalAlignment(Legend.LegendHorizontalAlignment.RIGHT)
        legend.setOrientation(Legend.LegendOrientation.HORIZONTAL)
        legend.setDrawInside(false)

        var legenedEntries = arrayListOf<LegendEntry>()
        legenedEntries.add(LegendEntry("DAY AHEAD TOTAL LOAD FORECAST", Legend.LegendForm.SQUARE, 8f, 8f, null, Color.CYAN))
        legenedEntries.add(LegendEntry("ACTUAL TOTAL LOAD", Legend.LegendForm.SQUARE, 8f, 8f, null, Color.BLUE))
        legend.setCustom(legenedEntries)

        legend.setYOffset(2f)
        legend.setXOffset(2f)
        legend.setYEntrySpace(0f)
        legend.setTextSize(9f)

        val xAxis = barChartView.getXAxis()
        xAxis.setGranularity(1f)
        xAxis.setGranularityEnabled(true)
        xAxis.setCenterAxisLabels(true)
        xAxis.setDrawGridLines(false)
//        xAxis.textSize = 10f
//
        xAxis.setPosition(XAxis.XAxisPosition.BOTTOM)
        xAxis.setValueFormatter(IndexAxisValueFormatter(xAxisValues))
        xAxis.setLabelCount(xAxisValues.size*2)
        Log.d("hey",xAxisValues.size.toString())
////        xAxis.setAvoidFirstLastClipping(true)
        barChartView.setDragEnabled(true)

        //Y-axis
        barChartView.getAxisRight().setEnabled(false)
        barChartView.setScaleEnabled(true)

        val leftAxis = barChartView.getAxisLeft()
        leftAxis.setValueFormatter(LargeValueFormatter())
        leftAxis.setDrawGridLines(false)
        leftAxis.setSpaceTop(1f)
        leftAxis.spaceBottom=88f
        leftAxis.setAxisMinimum(0f)
        barChartView.data = barData
        barChartView.setVisibleXRange(1f, 18f)
    }
}
