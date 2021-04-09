package com.cge.cgeenergy.interfaces

import com.cge.cgeenergy.models.*
import retrofit2.Call
import retrofit2.http.*

//interface Api {
//
//    @GET("Login")
//    fun login(@Query("username") username: String, @Query("password") password: String): Call<List<LoginResponse>>
//
//
//}
//interface Api {
////

////}
interface Api {
//    @POST("Login")
//    fun login(@Header("Authorization") authorization: String): Call<LoginResponse>
    @POST("Login")
    @FormUrlEncoded
    fun login(@Field("username") username: String, @Field("password") password: String): Call<LoginResponse>


    @GET("ActualTotalLoad/{areaName}/{resolution}/{datetype}/{date}")
    fun getactualtotalloadyear(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String, @Path("datetype") datetype: String, @Path("date") date: String):Call<List<Actual_response_year>>
    @GET("ActualTotalLoad/{areaName}/{resolution}/{datetype}/{date}")
    fun getactualtotalloadmonth(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Actual_response_month>>
    @GET("ActualTotalLoad/{areaName}/{resolution}/{datetype}/{date}")
    fun getactualtotalloaddate(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Actual_response_date>>

    @GET("AggregatedGenerationPerType/{areaName}/{productionType}/{resolution}/{datetype}/{date}")
    fun getaggregatedgenerationpertypeyear(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String,@Path("productionType") productionType: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Aggregated_response_year>>
    @GET("AggregatedGenerationPerType/{areaName}/{productionType}/{resolution}/{datetype}/{date}")
    fun getaggregatedgenerationpertypemonth(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String,@Path("productionType") productionType: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Aggregated_response_month>>
    @GET("AggregatedGenerationPerType/{areaName}/{productionType}/{resolution}/{datetype}/{date}")
    fun getaggregatedgenerationpertypedate(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String,@Path("productionType") productionType: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Aggregated_response_date>>

    @GET("DayAheadTotalLoadForecast/{areaName}/{resolution}/{datetype}/{date}")
    fun getdayaheadtotalloadyear(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Day_response_year>>
    @GET("DayAheadTotalLoadForecast/{areaName}/{resolution}/{datetype}/{date}")
    fun getdayaheadtotalloadmonth(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Day_response_month>>
    @GET("DayAheadTotalLoadForecast/{areaName}/{resolution}/{datetype}/{date}")
    fun getdayaheadtotalloaddate(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<Day_response_date>>

    @GET("ActualvsForecast/{areaName}/{resolution}/{datetype}/{date}")
    fun getavsftotalloadyear(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<AvsF_response_year>>
    @GET("ActualvsForecast/{areaName}/{resolution}/{datetype}/{date}")
    fun getavsftotalloadmonth(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<AvsF_response_month>>
    @GET("ActualvsForecast/{areaName}/{resolution}/{datetype}/{date}")
    fun getavsftotalloaddate(@Header("X-OBSERVATORY-AUTH") token:String,@Path("areaName") areaName: String, @Path("resolution") resolution: String,@Path("datetype") datetype: String, @Path("date") date: String):Call<List<AvsF_response_date>>

}
