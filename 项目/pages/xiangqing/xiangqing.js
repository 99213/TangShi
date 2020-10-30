// pages/xiangqing/xiangqing.js
Page({
  data: {
    isLike: true,
    // banner
    imgUrls: [
      "http://mz.djmall.xmisp.cn/files/product/20161201/148057921620_middle.jpg",
      "http://mz.djmall.xmisp.cn/files/product/20161201/148057922659_middle.jpg",
      "http://mz.djmall.xmisp.cn/files/product/20161201/148057923813_middle.jpg",
      "http://mz.djmall.xmisp.cn/files/product/20161201/148057924965_middle.jpg",
      "http://mz.djmall.xmisp.cn/files/product/20161201/148057925958_middle.jpg"
    ],
    indicatorDots: true, //是否显示面板指示点
    autoplay: true, //是否自动切换
    interval: 3000, //自动切换时间间隔,3s
    duration: 1000, //	滑动动画时长1s

    
  },
  
  // 收藏
  addLike() {
    this.setData({
      isLike: !this.data.isLike,
      })
  },
  // 跳到购物车
  addCar() {
    wx.showToast({
      title: '收藏成功',
      icon: 'success',
      duration: 2000
    });
  },
  // 立即购买
  immeBuy() {
    wx.switchTab({
      url: '/pages/dingdan/dingdan'
    });
    wx.showToast({
      title: '预约成功',
      icon: 'success',
      duration: 2000
    });
  },
})
