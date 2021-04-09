package com.cge.cgeenergy.managers

import com.cge.cgeenergy.interfaces.Api
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RequestManager {
    val interceptor = HttpLoggingInterceptor()
    val client = OkHttpClient.Builder().addInterceptor(interceptor).build()


    init {
        //TODO must be None at live
        interceptor.level = HttpLoggingInterceptor.Level.BODY
    }

//TODO: Change this
    val retrofit = Retrofit.Builder()
        .baseUrl("http://54195ade.ngrok.io/energy/api/")
        .addConverterFactory(GsonConverterFactory.create())
        .client(client)
        .build()

    val service = retrofit.create(Api::class.java)

}