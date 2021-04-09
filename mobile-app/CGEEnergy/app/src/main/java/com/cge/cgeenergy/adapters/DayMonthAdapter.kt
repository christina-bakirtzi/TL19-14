package com.cge.cgeenergy.adapters



import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.cge.cgeenergy.R
import com.cge.cgeenergy.models.Day_response_month

class DayMonthAdapter(private val myDataset: List<Day_response_month>) :
    RecyclerView.Adapter<DayMonthAdapter.MyViewHolder>() {

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
        holder.view.findViewById<TextView>(R.id.t7).text = myDataset[position].year
        holder.view.findViewById<TextView>(R.id.t8).text = myDataset[position].month
        holder.view.findViewById<TextView>(R.id.t9).text = myDataset[position].day
        holder.view.findViewById<TextView>(R.id.t10).text = myDataset[position].dayAheadTotalLoadForecastByDayValue
        holder.view.findViewById<TextView>(R.id.t11).visibility = View.GONE
        holder.view.findViewById<TextView>(R.id.t12).visibility = View.GONE
        holder.view.findViewById<TextView>(R.id.t13).visibility = View.GONE
    }


    override fun getItemCount() = myDataset.size
}