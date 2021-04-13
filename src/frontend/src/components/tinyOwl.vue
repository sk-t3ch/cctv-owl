<template>
  <div class="pretendBody">
    <div class="pretendContainer">
      <div class="ear1"></div>
      <div class="ear2"></div>
      <div class="prx owl-head">
        <div class="pax flx eye eye1">
          <div class="pax eye-inside">
            <div class="half-circle"></div>
          </div>
        </div>
        <div class="pax frx eye eye2">
          <div class="pax eye-inside">
            <div class="half-circle"></div>
          </div>
        </div>
        <div class="nose"></div>
      </div>
      <div class="cf">
        <div class="flx owl-leg leg1"></div>
        <div class="flx owl-leg leg2"></div>
      </div>
      <div class="prx branch"></div>
      <div class="text-center subtitle-1 secondary">
        CCTV OWL
      </div>
    </div>
  </div>
</template>
<style scoped>
/*#9CC873
#05060B
#4D391E
#F4D731*/
.pretendBody {
  padding: 0;
  margin: 0;
  background-color: black;
}

.cf:after {
  clear: both;
  content: " ";
  display: block;
}
.pretendContainer {
  width: 120px;
  height: 140px;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto;
}
.prx {
  position: relative;
}
.pax {
  position: absolute;
}
.flx {
  float: left;
}
.frx {
  float: right;
}
.owl-head {
  background-color: var(--v-secondary-base);
  border: 8px solid black;
  height: 110px;
  width: 110px;
  border-radius: 50%;
  overflow: hidden;
  left: 2px;
}
.owl-head .eye {
  width: 50px;
  height: 50px;
  margin-top: 20px;
  border-radius: 50%;
  border: 8px solid black;
  overflow: hidden;
}
.owl-head .eye1 {
  left: -2px;
}
.owl-head .eye2 {
  right: -2px;
}
.owl-head .eye-inside {
  background-color: var(--v-accent-base);
  width: 137%;
  height: 32px;
  border: 6px solid black;
  left: -7px;
  bottom: -8px;
  border-radius: 2px;
  overflow: hidden;
}
.owl-head .eye-inside .half-circle {
  background-color: black;
  height: 24px;
  width: 22px;
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
@keyframes move_eyes {
  0% {
    margin: -18px 9px;
  }
  20% {
    margin: -18px -3px;
  }
  40% {
    margin: -18px 9px;
  }
  60% {
    margin: -18px 23px;
  }
  80% {
    margin: -18px 9px;
  }
  100% {
    margin: -18px 9px;
  }
}

@-webkit-keyframes move_eyes {
  0% {
    margin: -18px 9px;
  }
  20% {
    margin: -18px -3px;
  }
  40% {
    margin: -18px 9px;
  }
  60% {
    margin: -18px 23px;
  }
  80% {
    margin: -18px 9px;
  }
  100% {
    margin: -18px 9px;
  }
}
.nose {
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 20px solid black;
  margin: 50px auto;
}
.owl-leg {
  background-color: black;
  width: 8px;
  height: 15px;
}
.owl-leg.leg1 {
  margin: -5px 0 0 45px;
}
.owl-leg.leg2 {
  margin: -5px 0 0 10px;
}
.branch {
  background-color: black;
  height: 8px;
  width: 100%;
  box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.3);
}
.branch:before {
  content: "";
  background-color: black;
  border-radius: 50%;
  height: 15px;
  width: 15px;
  position: absolute;
  left: -3px;
  top: -3px;
}

.branch:after {
  content: "";
  background-color: black;
  border-radius: 50%;
  height: 15px;
  width: 15px;
  position: absolute;
  right: -3px;
  top: -3px;
}
.ear1 {
  width: 0;
  height: 0;
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-bottom: 20px solid black;
  position: absolute;
  left: 7px;
  top: 7px;
  transform: rotate(-40deg);
  -moz-transform: rotate(-40deg);
  -webkit-transform: rotate(-40deg);
  -o-transform: rotate(-40deg);
  -ie-transform: rotate(-40deg);
}
.ear2 {
  width: 0;
  height: 0;
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-bottom: 20px solid black;
  position: absolute;
  right: 12px;
  top: 7px;
  transform: rotate(40deg);
  -moz-transform: rotate(40deg);
  -webkit-transform: rotate(40deg);
  -o-transform: rotate(40deg);
  -ie-transform: rotate(40deg);
}
</style>