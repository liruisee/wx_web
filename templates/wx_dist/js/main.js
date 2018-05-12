document.getElementsByTagName("html")[0].style.fontSize=document.documentElement.clientWidth/16+"px";//改变窗口的时候重新计算大小
window.onresize = function(){document.getElementsByTagName("html")[0].style.fontSize=document.documentElement.clientWidth/16+"px";}

var tea_type = {
    's':'上忍',
    'a':'老师',
    'r':'演员'
}

var child = {
    props:['img_url','teacher_id','teacher_name','teacher_record','teacher_type','video_url'],
    template:'<li @click="jump(teacherId)"><img :src=imgUrl alt="" class="box_list_img"><span class="teachername">{{ teacherName }}</span></li>',
    data:function(){
        return {
            'imgUrl':this.img_url,
            'teacherId':this.teacher_id,
            'teacherName':this.teacher_name,
            'teacherRecord':this.teacher_record,
            'teacherType':this.teacher_type,
            'videoUrl':this.video_url
        }
    },
    methods:{
        jump:function(e){
            console.log(e);
        }
    }
}