package com.cge.cgeenergy.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.cge.cgeenergy.R
import com.cge.cgeenergy.models.Actual_response_date

class ActualDateAdapter(private val myDataset: List<Actual_response_date>) :
    RecyclerView.Adapter<ActualDateAdapter.MyViewHolder>() {

    class MyViewHolder(val view: View) : RecyclerView.ViewHolder(view)
    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): MyViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.actual_date_row, parent, false)
        return MyViewHolder(view)
    }

    // Replace the contents of a view (invoked by the layout manager)
    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
//        holder.view.findViewById<TextView>(R.id.t1).text = myDataset[position].source
//        holder.view.findViewById<TextView>(R.id.t2).text = myDataset[position].dataset
//        holder.view.findViewById<TextView>(R.id.t3).text = myDataset[position].areaName
//        holder.view.findViewById<TextView>(R.id.t4).text = myDataset[position].areaTypeCode
//        holder.view.findViewById<TextView>(R.id.t5).text = myDataset[position].mapCode
//        holder.view.findViewById<TextView>(R.id.t6).text = myDataset[position].resolutionCode
        holder.view.findViewById<TextView>(R.id.t7).text = myDataset[position].year
        holder.view.findViewById<TextView>(R.id.t8).text = myDataset[position].month
        holder.view.findViewById<TextView>(R.id.t9).text = myDataset[position].day
        holder.view.findViewById<TextView>(R.id.t10).text = myDataset[position].dateTimeUTC
        holder.view.findViewById<TextView>(R.id.t11).text = myDataset[position].actualTotalLoadValue
        holder.view.findViewById<TextView>(R.id.t12).text = myDataset[position].updateTimeUTC
        holder.view.findViewById<TextView>(R.id.t13).visibility = View.GONE

    }


    override fun getItemCount() = myDataset.size
}