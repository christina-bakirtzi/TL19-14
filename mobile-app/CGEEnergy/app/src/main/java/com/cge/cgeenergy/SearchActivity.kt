package com.cge.cgeenergy

import android.app.AlertDialog
import android.content.DialogInterface
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.cge.cgeenergy.managers.DataManager
import com.cge.cgeenergy.managers.RequestManager
import com.cge.cgeenergy.models.*
import kotlinx.android.synthetic.main.activity_search.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class SearchActivity : AppCompatActivity() {
    private var token: String = ""
    val TOKENPREFSKEY = "tokenprefskey"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search)

        ////TOKEN
        val pref = applicationContext.getSharedPreferences("CGEEnergy", 0)
        token = pref.getString(TOKENPREFSKEY, "")!!


        val table = resources.getStringArray(R.array.array_tables)

        // Get radio group selected item using on checked change listener
        radio_group.setOnCheckedChangeListener(
            RadioGroup.OnCheckedChangeListener { group, checkedId ->
                val radio: RadioButton = findViewById(checkedId)
                Toast.makeText(
                    applicationContext,
                    " On checked change :" + " ${radio.text}",
                    Toast.LENGTH_SHORT
                ).show()
                if (checkedId == R.id.year_button) {
                    year_edittext.setVisibility(View.VISIBLE)
                    month_edittext.setVisibility(View.GONE)
                    date_edittext.setVisibility(View.GONE)
                }
                if (checkedId == R.id.month_button) {
                    month_edittext.setVisibility(View.VISIBLE)
                    year_edittext.setVisibility(View.GONE)
                    date_edittext.setVisibility(View.GONE)
                }
                if (checkedId == R.id.day_button) {
                    date_edittext.setVisibility(View.VISIBLE)
                    month_edittext.setVisibility(View.GONE)
                    year_edittext.setVisibility(View.GONE)
                }
            })

        // Get radio group selected status and text using button click event


        val tables = resources.getStringArray(R.array.array_tables)
        val spinner = findViewById<Spinner>(R.id.spinner1)
        if (spinner != null) {
            val adapter = ArrayAdapter(
                this,
                android.R.layout.simple_spinner_item, tables
            )
            spinner.adapter = adapter

            spinner.onItemSelectedListener = object :
                AdapterView.OnItemSelectedListener {
                override fun onItemSelected(
                    parent: AdapterView<*>,
                    view: View, position: Int, id: Long
                ) {
                    if (tables[position] == "Aggregated Generation Per Type") {
                        productiontype_edittext.setVisibility(View.VISIBLE)
                    } else {
                        productiontype_edittext.setVisibility(View.GONE)
                    }

                    Toast.makeText(
                        this@SearchActivity,
                        getString(R.string.selected_item) + " " + "" + tables[position],
                        Toast.LENGTH_SHORT
                    ).show()
                }

                override fun onNothingSelected(parent: AdapterView<*>) {
                    // write code to perform some action
                }
            }

        }

        val resolutions = resources.getStringArray(R.array.array_resolutions)
        val spinner_resolution = findViewById<Spinner>(R.id.spinner_resolution)

        if (spinner_resolution != null) {
            val adapter = ArrayAdapter(
                this,
                android.R.layout.simple_spinner_item, resolutions
            )
            spinner_resolution.adapter = adapter

            spinner_resolution.onItemSelectedListener = object :
                AdapterView.OnItemSelectedListener {
                override fun onItemSelected(
                    parent: AdapterView<*>,
                    view: View, position: Int, id: Long
                ) {
                    Toast.makeText(
                        this@SearchActivity,
                        getString(R.string.selected_item) + " " +
                                "" + resolutions[position], Toast.LENGTH_SHORT
                    ).show()
                }

                override fun onNothingSelected(parent: AdapterView<*>) {
                    // write code to perform some action
                }
            }

        }


        //THE CALLS

        btnSubmit.setOnClickListener {
            var datetype = " "
            var date = " "
            var productiontype = " "
            val areaName = areaname_edittext.text.toString()
            val resolution = spinner_resolution.selectedItem.toString()
            productiontype = productiontype_edittext.text.toString()
            if (radio_group.checkedRadioButtonId == R.id.year_button) {
                datetype = "year"
                date = year_edittext.text.toString()
            } else if (radio_group.checkedRadioButtonId == R.id.month_button) {
                datetype = "month"
                date = month_edittext.text.toString()
            } else if (radio_group.checkedRadioButtonId == R.id.day_button) {
                datetype = "date"
                date = date_edittext.text.toString()
            }
            var table = " "
            if (spinner.selectedItem.toString() == "Actual Total Load") {
                table = "ActualTotalLoad"
            } else if (spinner.selectedItem.toString() == "Aggregated Generation Per Type") {
                table = "AggregatedGenerationPerType"
            } else if (spinner.selectedItem.toString() == "Day-Ahead Total Load Forecast") {
                table = "DayAheadTotalLoadForecast"
            } else if (spinner.selectedItem.toString() == "Actual Total Load vs Day-Ahead Total Load Forecast") {
                table = "ActualvsForecast"
            }
            if (spinner.selectedItem.toString() == "Actual Total Load") {
                if (datetype == "year") {
                    val call = RequestManager.service.getactualtotalloadyear(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Actual_response_year>> {
                        override fun onResponse(
                            call: Call<List<Actual_response_year>>,
                            response: Response<List<Actual_response_year>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Actual Total Load"
                                DataManager.actualYearResponse = response.body()
                                openActualYearActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(
                            call: Call<List<Actual_response_year>>,
                            t: Throwable
                        ) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "month") {
                    val call = RequestManager.service.getactualtotalloadmonth(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Actual_response_month>> {
                        override fun onResponse(
                            call: Call<List<Actual_response_month>>,
                            response: Response<List<Actual_response_month>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Actual Total Load"
                                DataManager.actualMonthResponse = response.body()
                                openActualMonthActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(
                            call: Call<List<Actual_response_month>>,
                            t: Throwable
                        ) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "date") {
                    val call = RequestManager.service.getactualtotalloaddate(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Actual_response_date>> {
                        override fun onResponse(
                            call: Call<List<Actual_response_date>>,
                            response: Response<List<Actual_response_date>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Actual Total Load"
                                DataManager.actualDateResponse = response.body()
                                openTableActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(
                            call: Call<List<Actual_response_date>>,
                            t: Throwable
                        ) {
                            loaderout.visibility = View.GONE
                        }
                    })
                }
            }//endif
            else if (spinner.selectedItem.toString() == "Aggregated Generation Per Type") {
                if (datetype == "year") {
                    val call = RequestManager.service.getaggregatedgenerationpertypeyear(
                        token,
                        areaName,
                        productiontype,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Aggregated_response_year>> {
                        override fun onResponse(
                            call: Call<List<Aggregated_response_year>>,
                            response: Response<List<Aggregated_response_year>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Aggregated Generation Per Type"
                                DataManager.aggregatedYearResponse = response.body()
                                openAggregatedYearActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(
                            call: Call<List<Aggregated_response_year>>,
                            t: Throwable
                        ) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "month") {
                    val call = RequestManager.service.getaggregatedgenerationpertypemonth(
                        token,
                        areaName,
                        productiontype,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Aggregated_response_month>> {
                        override fun onResponse(
                            call: Call<List<Aggregated_response_month>>,
                            response: Response<List<Aggregated_response_month>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Aggregated Generation Per Type"
                                DataManager.aggregatedMonthResponse = response.body()
                                openAggregatedMonthActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            }else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            } else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(
                            call: Call<List<Aggregated_response_month>>,
                            t: Throwable
                        ) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "date") {
                    val call = RequestManager.service.getaggregatedgenerationpertypedate(
                        token,
                        areaName,
                        productiontype,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Aggregated_response_date>> {
                        override fun onResponse(
                            call: Call<List<Aggregated_response_date>>,
                            response: Response<List<Aggregated_response_date>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Aggregated Generation Per Type"
                                DataManager.aggregatedDateResponse = response.body()
                                openAggregatedDateActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(
                            call: Call<List<Aggregated_response_date>>,
                            t: Throwable
                        ) {
                            loaderout.visibility = View.GONE
                        }
                    })
                }
            }//endif
            else if (spinner.selectedItem.toString() == "Day-Ahead Total Load Forecast") {
                if (datetype == "year") {
                    val call = RequestManager.service.getdayaheadtotalloadyear(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Day_response_year>> {
                        override fun onResponse(
                            call: Call<List<Day_response_year>>,
                            response: Response<List<Day_response_year>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Day-Ahead Total Load Forecast"
                                DataManager.dayYearResponse = response.body()
                                openDayYearActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(call: Call<List<Day_response_year>>, t: Throwable) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "month") {
                    val call = RequestManager.service.getdayaheadtotalloadmonth(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Day_response_month>> {
                        override fun onResponse(
                            call: Call<List<Day_response_month>>,
                            response: Response<List<Day_response_month>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Day-Ahead Total Load Forecast"
                                DataManager.dayMonthResponse = response.body()
                                openDayMonthActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            }else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            } else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(call: Call<List<Day_response_month>>, t: Throwable) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "date") {
                    val call = RequestManager.service.getdayaheadtotalloaddate(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<Day_response_date>> {
                        override fun onResponse(
                            call: Call<List<Day_response_date>>,
                            response: Response<List<Day_response_date>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable = "Day-Ahead Total Load Forecast"
                                DataManager.dayDateResponse = response.body()
                                openDayDateActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            }  else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(call: Call<List<Day_response_date>>, t: Throwable) {
                            loaderout.visibility = View.GONE
                        }
                    })
                }
            }//endif
            else if (spinner.selectedItem.toString() == "Actual Total Load vs Day-Ahead Total Load Forecast") {
                if (datetype == "year") {
                    val call = RequestManager.service.getavsftotalloadyear(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<AvsF_response_year>> {
                        override fun onResponse(
                            call: Call<List<AvsF_response_year>>,
                            response: Response<List<AvsF_response_year>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable =
                                    "Actual Total Load vs Day-Ahead Total Load Forecast"
                                DataManager.avsfYearResponse = response.body()
                                openAvsFYearActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(call: Call<List<AvsF_response_year>>, t: Throwable) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "month") {
                    val call = RequestManager.service.getavsftotalloadmonth(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<AvsF_response_month>> {
                        override fun onResponse(
                            call: Call<List<AvsF_response_month>>,
                            response: Response<List<AvsF_response_month>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable =
                                    "Actual Total Load vs Day-Ahead Total Load Forecast"
                                DataManager.avsfMonthResponse = response.body()
                                openAvsFMonthActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(
                            call: Call<List<AvsF_response_month>>,
                            t: Throwable
                        ) {
                            loaderout.visibility = View.GONE
                        }
                    })
                } else if (datetype == "date") {
                    val call = RequestManager.service.getavsftotalloaddate(
                        token,
                        areaName,
                        resolution,
                        datetype,
                        date
                    )
                    loaderout.visibility = View.VISIBLE
                    call.enqueue(object : Callback<List<AvsF_response_date>> {
                        override fun onResponse(
                            call: Call<List<AvsF_response_date>>,
                            response: Response<List<AvsF_response_date>>
                        ) {
                            loaderout.visibility = View.GONE
                            if (response.isSuccessful) {
                                DataManager.selectedTable =
                                    "Actual Total Load vs Day-Ahead Total Load Forecast"
                                DataManager.avsfDateResponse = response.body()
                                openAvsFDateActivity()
                            } else if (response.code() == 401) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Not authorized", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 402) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Try again later", Toast.LENGTH_SHORT
                                ).show()
                            } else if (response.code() == 400) {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "Wrong input form", Toast.LENGTH_SHORT
                                ).show()
                            }else {
                                Toast.makeText(
                                    this@SearchActivity,
                                    "No data found", Toast.LENGTH_SHORT
                                ).show()
                            }
                        }

                        override fun onFailure(call: Call<List<AvsF_response_date>>, t: Throwable) {
                            loaderout.visibility = View.GONE
                        }
                    })
                }
            }
//            val call = RequestManager.service.getactualtotalloadyear(areaName, resolution, datetype, date)
//            loaderout.visibility = View.VISIBLE
//            call.enqueue(object : Callback<List<Actual_response_year>> {
//                override fun onResponse(
//                    call: Call<List<Actual_response_year>>,
//                    response: Response<List<Actual_response_year>>
//                ) {
//                    loaderout.visibility = View.GONE
//                    if (response.isSuccessful) {
//                        val listOfModels =

//                        if (listOfModels != null) {
//                            for ((index, model) in listOfModels.withIndex()) {
//                                Log.d("----", "----")
//                                Log.d(
//                                    "INDEX $index",
//                                    "ActualTotalLoadByMonthValue ${model.actualTotalLoadByMonthValue}"
//                                )
//                                Log.d("INDEX $index", "AreaName ${model.areaName}")
//                                Log.d("INDEX $index", "AreaTypeCode ${model.areaTypeCode}")
//                                Log.d("INDEX $index", "Dataset ${model.dataset}")
//                                Log.d("INDEX $index", "MapCode ${model.mapCode}")
//                                Log.d("INDEX $index", "Month ${model.month}")
//                                Log.d("INDEX $index", "ResolutionCode ${model.resolutionCode}")
//                                Log.d("INDEX $index", "Source ${model.source}")
//                                Log.d("INDEX $index", "Year ${model.year}")
//                                Log.d("----", "----")
//                            }
//                            openTableActivity()
//                        } else {
//                            Toast.makeText(
//                                this@SearchActivity,
//                                "No data found", Toast.LENGTH_SHORT
//                            ).show()
//                        }
//                    } else {
//                        Toast.makeText(
//                            this@SearchActivity,
//                            "No data found", Toast.LENGTH_SHORT
//                        ).show()
//
//                    }
//                }
//
//                override fun onFailure(call: Call<List<Actual_response_year>>, t: Throwable) {
//                    loaderout.visibility = View.GONE
//                }
//            })
            var id: Int = radio_group.checkedRadioButtonId
            if (id != -1) { // If any radio button checked from radio group
                // Get the instance of radio button using id
                val radio: RadioButton = findViewById(id)
                Toast.makeText(
                    applicationContext,
                    "On button click :" + " ${radio.text}",
                    Toast.LENGTH_SHORT
                ).show()
            } else {
                // If no radio button checked in this radio group
                Toast.makeText(
                    applicationContext,
                    "On button click :" + " nothing selected",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }


        logout_button.setOnClickListener {
            val dialogBuilder = AlertDialog.Builder(this)
            dialogBuilder.setMessage("Are you sure you want to logout?")
                .setCancelable(false)
                .setPositiveButton("Yes", DialogInterface.OnClickListener { dialog, id ->
                    logoutbuttonclicked()
                })
                .setNegativeButton("Cancel", DialogInterface.OnClickListener { dialog, id ->
                    dialog.cancel()
                })

            val alert = dialogBuilder.create()
            alert.setTitle("LOGOUT")
            alert.show()
        }
    }


    private fun openActualYearActivity() {
        val intent = Intent(this, ActualYearActivity::class.java)
        startActivity(intent)
    }

    private fun openActualMonthActivity() {
        val intent = Intent(this, ActualMonthActivity::class.java)
        startActivity(intent)
    }

    private fun openDayYearActivity() {
        val intent = Intent(this, DayYearActivity::class.java)
        startActivity(intent)
    }

    private fun openDayMonthActivity() {
        val intent = Intent(this, DayMonthActivity::class.java)
        startActivity(intent)
    }

    private fun openDayDateActivity() {
        val intent = Intent(this, DayDateActivity::class.java)
        startActivity(intent)
    }

    private fun openAggregatedYearActivity() {
        val intent = Intent(this, AggregatedYearActivity::class.java)
        startActivity(intent)
    }

    private fun openAggregatedMonthActivity() {
        val intent = Intent(this, AggregatedMonthActivity::class.java)
        startActivity(intent)
    }

    private fun openAggregatedDateActivity() {
        val intent = Intent(this, AggregatedDateActivity::class.java)
        startActivity(intent)
    }

    private fun openAvsFYearActivity() {
        val intent = Intent(this, AvsFYearActivity::class.java)
        startActivity(intent)
    }

    private fun openAvsFMonthActivity() {
        val intent = Intent(this, AvsFMonthActivity::class.java)
        startActivity(intent)
    }

    private fun openAvsFDateActivity() {
        val intent = Intent(this, AvsFDateActivity::class.java)
        startActivity(intent)
    }

    private fun openTableActivity() {
        val intent = Intent(this, TableActivity::class.java)
        startActivity(intent)
//        finish()
    }

    fun radio_button_click(view: View) {
        // Get the clicked radio button instance
        val radio: RadioButton = findViewById(radio_group.checkedRadioButtonId)
        Toast.makeText(applicationContext, "Search per : ${radio.text}", Toast.LENGTH_SHORT).show()
    }

    private fun logoutbuttonclicked() {
        Log.d(
            "logged_oute",
            "button clicked "
        )
        loaderout.visibility = View.VISIBLE
        applicationContext.getSharedPreferences("CGEEnergy", 0).edit().clear().apply()
        finishAffinity()
        startActivity(Intent(this, MainActivity::class.java))

    }

    override fun onResume() {
        super.onResume()
    }
}
