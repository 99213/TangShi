// pages/zhuye/zhuye.js

Page({

  /**
   * 页面的初始数据
   */
  data: {
      array:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
     var array = this.initData();
     this.setData({array:array});
  },
  initData:function(){
    var array = [];
    var object1 = new Object();
    object1.img = '/images/image-zhuye-mixian.jpg';
    object1.title = '虾饺米线';
    object1.type = '8元一碗'
    object1.liulan='15浏览';
    object1.pinglun='2评论';
    array[0] = object1;
  
    var object2 = new Object();
    object2.img = '/images/image-zhuye-shaguo.jpg';
    object2.title = '砂锅';
    object2.type= '10元一碗'
    object2.liulan='39浏览';
    object2.pinglun='5评论';
    array[1] = object2;
    return array;
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

  }
})