document.getElementsByTagName("html")[0].style.fontSize=document.documentElement.clientWidth/16+"px";//改变窗口的时候重新计算大小
window.onresize = function(){document.getElementsByTagName("html")[0].style.fontSize=document.documentElement.clientWidth/16+"px";}

//针对url发送数据处理
var aValue = [];//url参数列表
function fnUrlData(){
  var curUrl = location.href;
  if(curUrl.indexOf('?') != -1){
    var strData = curUrl.split('?')[1];
    var Adata = strData.split('&');
    var dataLen = Adata.length;
    for(var i=0;i<dataLen;i++){
      aValue.push(Adata[i].split('=')[1]);
    }
    return aValue;
  }
}


var typeListchild = {
    props:['img_url','teacher_id','teacher_name','teacher_record','teacher_type','video_url'],
    template:'<li @click="jump(teacherId)"><img v-bind:src=imgsrc alt="" class="box_list_img"><span class="teachername">{{ teacherName }}</span></li>',
    data:function(){
        return {
            'imgUrl':this.img_url,
            'teacherId':this.teacher_id,
            'teacherName':this.teacher_name,
            'teacherRecord':this.teacher_record,
            'teacherType':this.teacher_type,
            'videoUrl':this.video_url,
            'imgsrc':'images/'+this.img_url
        }
    },
    methods:{
        jump:function(e){
            console.log(e);
        }
    }
}

var teacherlistchild = {
    props:['img_url','teacher_id','teacher_name','teacher_record','teacher_type','video_url'],
    template:'<li><div class="teacher_list_img"><img v-bind:src=imgsrc alt=""></div><div class="teacher_list_msg"><p class="list_msg_name">{{teacherName}}</p><p class="list_msg_type"><span>类别：</span>{{teacherType}}</p><p class="list_msg_brief"><span>简介：</span>{{teacherRecord}}</p></div></li>',
    data:function(){
        return {
            'imgUrl':this.img_url,
            'teacherId':this.teacher_id,
            'teacherName':this.teacher_name,
            'teacherRecord':this.teacher_record,
            'teacherType':this.teacher_type,
            'videoUrl':this.video_url,
            'imgsrc':'images/'+this.img_url
        }
    },
}