      
 //index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    wx.getUserInfo({
      success: this.setUserInfo.bind(this)
    })
    this.setData({
      
    })
   
  },
  setUserInfo: function (res) {
    this.setData({ user: res.userInfo })
  },

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
  create_login: function (e) {
    console.log(e.detail.value)
    wx.request({
      url: "http://127.0.0.1:8000/trytest/sign/?" + "password=" + e.detail.value["password"] + "&phonenumber=" + e.detail.value["phonenumber"],
      //url地址为后端代码的位置需修改
      data: e.detail.value,
      success: this.getResult.bind(this)
    })
    
  },
  getResult: function (res) {
    console.log(res.data);
    if(res.data['status'] == 1){
    wx.showToast({
      title: "登录成功",
      duration: 2000
    })
      wx.switchTab({
        url: '../index/index',
      })
    setTimeout(function () {
      wx.navigateBack({
        delta: 2
      })
    }, 1000)
  }
  
  if(res.data == "false"){
    wx.showToast({
      title: "账号或密码不对",
      icon: 'none',
      duration: 3000
    })
    setTimeout(function () {
      wx.navigateBack({
        delta: 2
      })
    }, 1000)
  }
  },
  goto_yanzhengma:function(res){
    wx.navigateTo({
      url: '../yanzhengma/yanzhengma',
    })
  },
  goto_zhuce: function (res) {
    wx.navigateTo({
      url: '../zhuce/zhuce',
    })
  },
  login:function( e ){
    var that = this;
    if( !e.detail.userInfo ){
        app.alert( { 'content':'登录失败，请再次点击~~' } );
        return;
    }
    var data = e.detail.userInfo;
    wx.login({
        success:function( res ){
            if( !res.code ){
                app.alert( { 'content':'登录失败，请再次点击~~' } );
                return;
            }
            data['code'] = res.code;
            wx.request({
                url:app.buildUrl( '/member/login' ),
                header:app.getRequestHeader(),
                method:'POST',
                data:data,
                success:function( res ){
                    if( res.data.code != 200 ){
                        app.alert( { 'content':res.data.msg } );
                        return;
                    }
                    app.setCache( "token",res.data.data.token );
                    that.goToIndex();
                }
            });
        }
    });
}
})