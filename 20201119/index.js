Page({
  data: {
    value: ''
  },

  input(e) {
    this.data.value = e.detail.value
  },

  print() {
    const text = this.data.value
    console.log(text ? `你输入了：${text}` : '你还什么都没输入...')
  }
})
