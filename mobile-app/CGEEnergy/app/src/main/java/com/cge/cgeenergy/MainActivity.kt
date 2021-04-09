package com.cge.cgeenergy

import android.content.Intent
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import com.cge.cgeenergy.managers.RequestManager
import com.cge.cgeenergy.models.LoginResponse
import kotlinx.android.synthetic.main.activity_main.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        login_button.setOnClickListener {
            buttonClicked()
        }
        if (getTokenFromPrefs()?.length!! > 0) {
            openSearchActivity()
        }
    }

    private fun buttonClicked() {
        val username = username_edittext.text.toString()
        val password = password_edittext.text.toString()
        Log.d(
            "eeee",
            "button clicked " + username_edittext.text.toString() + " password " + password_edittext.text.toString()
        )
        loader.visibility = View.VISIBLE
        val authPayload = "$username:$password"
        val data = authPayload.toByteArray()
        val base64 = Base64.encodeToString(data, Base64.NO_WRAP)

//        val call = RequestManager.service.login("Basic $base64".trim())
        val call = RequestManager.service.login(username, password)
        call.enqueue(object : Callback <LoginResponse> {
            override fun onResponse(call: Call<LoginResponse>, response: Response<LoginResponse>)
            {
                loader.visibility = View.GONE
                if (response.isSuccessful) {
                    openSearchActivity()
                    saveTokenToPrefs(response.body().token)
                } else {

                }
            }

            override fun onFailure(call: Call<LoginResponse>, t: Throwable) {
                loader.visibility = View.GONE
            }
        })
    }

    val TOKENPREFSKEY = "tokenprefskey"
    private fun saveTokenToPrefs(token: String) {
        val pref = applicationContext.getSharedPreferences("CGEEnergy", 0)
        val editor = pref.edit()
        editor.putString(TOKENPREFSKEY, token)
        editor.commit()
    }

    private fun getTokenFromPrefs(): String? {
        val pref = applicationContext.getSharedPreferences("CGEEnergy", 0)
        return pref.getString(TOKENPREFSKEY, "")
    }

    private fun openSearchActivity() {
        val intent = Intent(this, SearchActivity::class.java)
        startActivity(intent)
        if (getTokenFromPrefs()?.length!! == 0) {
            openMainActivity()
        }
        finish()
    }

    private fun openMainActivity() {
        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)
        finish()
    }


}
