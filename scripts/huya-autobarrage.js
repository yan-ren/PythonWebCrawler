/*
Test with real broadcasting room:
if duration is 10,000, message will be blocked after 30 sent
if duration is 20,000, sent 462 messages without issue
*/


const area = document.getElementById('pub_msg_input')
const btn = document.getElementById('msg_send_bt')

const danmu = ["主播唱歌真好听",
               "主播跳舞真好看",
               "666",
               "喜欢主播的点点订阅",
               "送送小礼物卡牌子了",
               "喜欢主播的送送小礼物卡牌子了",
               "欢迎哥哥姐姐们来到直播间",
               "欢迎进入直播间",
               "喜欢主播的订阅走一走啦",
               "订阅走一走啦",
               "哥哥们虎粮走一波",
               "哈哈哈",
               "大哥们点点订阅啦",
               "谢谢大家的虎粮",
               "新主播支持一下啦",
               "弹幕扣起来",
               "气氛组上班了",
               "我是弹幕机器人",
               "虎粮走一走活到九十九，礼物刷一刷主播抱回家"]

let duration = 20000
let i = 0
let interval

function start() {
  interval = setInterval(function() {
    area.value = danmu[Math.floor(Math.random() * danmu.length)]
    let time=document.getElementsByClassName("msg_send_time")
    if (time[0]==undefined || time[0].innerHTML==0) {
      btn.setAttribute("class", "btn-sendMsg hiido_stat enable");
      btn.click()
      i++
    }
  }, duration)
}

function stop() {
  clearInterval(interval)
  console.log("sent:" + i)
  i = 0
}
