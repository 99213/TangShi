// pages/zhuce/zhuce.js
// pages/zhuce/zhuce.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  /*onLoad: function (options) {
    console.log(options)
    wx.getUserInfo({
      success: this.setUserInfo.bind(this)
    })
    this.setData({

    })
  },
  setUserInfo: function (res) {
    this.setData({ user: res.userInfo })
  },*/
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  create_zhuce: function (e) {
    console.log(e.detail.value)
    wx.request({
      url: "http://localhost:8000/trytest/register?" + "&password=" + e.detail.value["password1"] ,
      data: e.detail.value,
      success: this.getResult.bind(this)
    })

  },
  getResult: function (res) {
    console.log(res.data);
    if (res.data == "true") {
      wx.showToast({
        title: "注册成功",
        duration: 2000
      })
      wx.switchTab({
        url: '../login/login',
      })
      setTimeout(function () {
        wx.navigateBack({
          delta: 2
        })
      }, 2000)
    }

    if (res.data == "-1") {
      wx.showToast({
        title: "用户名已存在",
        icon: 'none',
        duration: 2000
      })
      setTimeout(function () {
        wx.navigateBack({
          delta: 2
        })
      }, 2000)
    }

    if (res.data == "1") {
      wx.showToast({
        title: "注册信息不为空",
        icon: 'none',
        duration: 2000
      })
      setTimeout(function () {
        wx.navigateBack({
          delta: 2
        })
      }, 2000)
    }

    if ((res.data == "false") || (res.data == "0")) {
      wx.showToast({
        title: "前后密码不一致",
        icon: 'none',
        duration: 3000
      })
      setTimeout(function () {
        wx.navigateBack({
          delta: 2
        })
      }, 2000)
    }
  },
  
})