<template>
  <div class="container">
    <div class="ear1"></div>
    <div class="ear2"></div>
    <div class="pr owl-head">
      <div class="pa fl eye eye1">
        <div class="pa eye-inside">
          <div class="half-circle"></div>
        </div>
      </div>
      <div class="pa fr eye eye2">
        <div class="pa eye-inside">
          <div class="half-circle"></div>
        </div>
      </div>
      <div class="nose"></div>
    </div>
    <div class="cf">
      <div class="fl owl-leg leg1"></div>
      <div class="fl owl-leg leg2"></div>
    </div>
    <div class="pr branch"></div>
  </div>
</template>
<style scoped>
/*#9CC873
#05060B
#4D391E
#F4D731*/
.cf:after{
  clear:both;
  content:' ';
  display:block;
}
.container{
  width: 120px;
  height: 140px;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto;
}
.pr{
  position: relative;
}
.pa{
  position: absolute;
}
.fl{
  float: left;
}
.fr{
  float: right;
}
.owl-head{
  background-color: #4D391E;
  border: 8px solid #05060B;
  height: 100px;
  width: 100px;
  border-radius: 50%;
  overflow: hidden;
}
.owl-head .eye{
  width: 42px;
  height: 42px;
  margin-top: 20px;
  border-radius: 50%;
  border: 8px solid #05060B;
  overflow: hidden;
}
.owl-head .eye1{
  left: -5px;
}
.owl-head .eye2{
  right: -5px;
}
.owl-head .eye-inside{
  background-color: #F4D731;
  width: 113%;
  height: 20px;
  border: 8px solid #05060B;
  left: -10px;
  bottom: -10px;
  border-radius: 2px;
  overflow: hidden;
}
.owl-head .eye-inside .half-circle{
  background-color: #05060B;
  height: 25px;
  width: 25px;
  border-radius: 50%;
  margin: -18px 9px;
  animation-name: move_eyes;
  animation-duration: 10s;
  animation-iteration-count: infinite;
  -o-animation-name: move_eyes;
  -o-animation-duration: 10s;
  -o-animation-iteration-count: infinite;
  -webkit-animation-name: move_eyes;
  -webkit-animation-duration: 10s;
  -webkit-animation-iteration-count: infinite;
  -ie-animation-name: move_eyes;
  -ie-animation-duration: 10s;
  -ie-animation-iteration-count: infinite;
}
@keyframes move_eyes{
  0%{ margin: -18px 9px; }
  20%{ margin: -18px -3px; }
  40%{ margin: -18px 9px; }
  60%{ margin: -18px 23px; }
  80%{ margin: -18px 9px; }
  100%{ margin: -18px 9px; }
}

@-webkit-keyframes move_eyes{
  0%{ margin: -18px 9px; }
  20%{ margin: -18px -3px; }
  40%{ margin: -18px 9px; }
  60%{ margin: -18px 23px; }
  80%{ margin: -18px 9px; }
  100%{ margin: -18px 9px; }
}
.nose{
  width: 0; 
  height: 0; 
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 20px solid #05060B;
  margin: 60px auto;
}
.owl-leg{
  background-color: #05060B;
  width: 8px;
  height: 15px;
}
.owl-leg.leg1{
  margin: -5px 0 0 45px;
}
.owl-leg.leg2{
  margin: -5px 0 0 10px;
}
.branch{
  background-color: #05060B;
  height: 8px;
  width: 100%;
  box-shadow: 0px 3px 3px rgba(0,0,0,.3)
}
.branch:before{
  content: '';
  background-color: #05060B;
  border-radius: 50%;
  height: 15px;
  width: 15px;
  position: absolute;
  left: -3px;
  top: -3px;
}

.branch:after{
  content: '';
  background-color: #05060B;
  border-radius: 50%;
  height: 15px;
  width: 15px;
  position: absolute;
  right: -3px;
  top: -3px;
}
.ear1{
  width: 0; 
  height: 0; 
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-bottom: 20px solid #05060B; 
  position: absolute;
  left: 0;
  top: 7px;
  transform: rotate(-40deg);
  -moz-transform: rotate(-40deg);
  -webkit-transform: rotate(-40deg);
  -o-transform: rotate(-40deg);
  -ie-transform: rotate(-40deg);
}
.ear2{
  width: 0; 
  height: 0; 
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-bottom: 20px solid #05060B; 
  position: absolute;
  right: 5px;
  top: 7px;
  transform: rotate(40deg);
  -moz-transform: rotate(40deg);
  -webkit-transform: rotate(40deg);
  -o-transform: rotate(40deg);
  -ie-transform: rotate(40deg);
}
</style>