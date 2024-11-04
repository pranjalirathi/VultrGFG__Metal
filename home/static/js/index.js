const StrForAuth=document.getElementById('get-from-here').innerText;
document.getElementById('get-from-here').innerText="";
document.getElementById('get-from-here').remove();
let element = document.querySelector('#search');
var data={};
element.addEventListener("click", calculate);
function calculate(event){
    event.preventDefault();
    let form = document.getElementById("myform");
    let inputs = form.getElementsByTagName("input");
    var chk=1;
    for (let i = 0; i < inputs.length; i++) {
      let input = inputs[i];
      if (input.hasAttribute("required") && input.value === "") {
        document.getElementById('warning').hidden = false;
        scrollTo(0, document.body.scrollHeight);
        chk=0;
        return
      }
      else {
          if (input.type === "number") data[input.id]=Number(input.value);
          else if (input.type==="radio") {
              if (input.checked) data[input.name]=input.value;
          }
        //   else if (input.id == "" && input.name=="csrfmiddlewaretoken" ) data["csrfmiddlewaretoken"] = input.value;
          else data[input.id]=input.value;
      }
    }
    if (data['target_weight']>data['weight']) data['goal']="gain";
    else if (data['target_weight'] < data['weight']) data['goal']="loose";
    else data['goal']='maintain';
    
    console.log(data); console.log(StrForAuth);
    //localhost:3000/calculate
    fetch('/calculate', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-Auth-Key': StrForAuth,
        'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value 
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        return response.json()
    })
    .then(result=> {
        document.getElementById('bmi').innerText = result['bmi'];
        document.getElementById(('category')).innerText = result['category'];
        document.getElementById('calories').innerText = result['calories'];
        document.getElementById('intake').innerText = `Per Day To Reach ${result['target_weight']} kgs`;
        document.getElementById('calories-intake').innerText = `${result['calories']} (+/-100)`;
        document.getElementById('carb').innerText = `${result['carb']}g`;
        document.getElementById('protein').innerText = `${result['protein']}g`;
        document.getElementById('fat').innerText = `${result['fat']}g`;
        document.getElementById('carb_per').style.width=`${result['carb_per']}%`;
        document.getElementById('protein_per').style.width=`${result['protein_per']}%`;
        document.getElementById('fat_per').style.width=`${result['fat_per']}%`;
        if (result['category']==="Healthy")document.getElementById(('category')).style.color = "#72ff78", document.getElementById('bmi').style.color="#72ff79";
        else document.getElementById(('category')).style.color = "#ff4c82", document.getElementById('bmi').style.color="#ff4c82";
        document.getElementById('intake').style.color = "#2bedff", document.getElementById('calories').style.color = "#2bedff";
        document.getElementById('note-in-macro').style.color="#ffaf1b";
        document.getElementById('carb_per').style.backgroundImage =`linear-gradient(to right, #0064ff, #0098ff, #00beff, #00ddec, #46f6ce)`;
        document.getElementById('protein_per').style.backgroundImage="linear-gradient(to right, #fb4557, #ff733d, #ffa124, #f9cd1f, #def646)";
        document.getElementById('fat_per').style.backgroundImage="linear-gradient(to right, #710fff, #ab2ff5, #d151ee, #ec73e9, #ff96e9)";
        document.getElementById('carb').style.cssText="background-image: linear-gradient(to right, #0064ff, #0098ff, #00beff, #00ddec, #46f6ce); -webkit-background-clip: text; -webkit-text-fill-color: transparent; -moz-background-clip: text; -moz-text-fill-color: transparent;";
        document.getElementById('protein').style.cssText="background-image: linear-gradient(to right, #fb4557, #ff733d, #ffa124, #f9cd1f, #def646); -webkit-background-clip: text; -webkit-text-fill-color: transparent; -moz-background-clip: text; -moz-text-fill-color: transparent;";
        document.getElementById('fat').style.cssText="background-image: linear-gradient(to right, #710fff, #ab2ff5, #d151ee, #ec73e9, #ff96e9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; -moz-background-clip: text; -moz-text-fill-color: transparent;";
        document.querySelector('.carb-before').style.cssText=" ";
        document.querySelector('.protein-before').style.cssText=" ";
        document.getElementsByClassName('fat-before')[0].style.cssText=" ";
        document.getElementById('warning').hidden=true;
        document.querySelector('.get-chart').style="";
    })
}
let element1 = document.querySelector('.get-chart');
element1.addEventListener("click", prepare);

function prepare(){
    document.querySelector('.chart-content').innerHTML=
    `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto; display: block;" width="200px" height="200px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
    <g transform="translate(20 50)">
    <circle cx="0" cy="0" r="6" fill="#456caa">
        <animateTransform attributeName="transform" type="scale" begin="-0.375s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
    </circle>
    </g><g transform="translate(40 50)">
    <circle cx="0" cy="0" r="6" fill="#88a2ce">
      <animateTransform attributeName="transform" type="scale" begin="-0.25s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
    </circle>
    </g><g transform="translate(60 50)">
    <circle cx="0" cy="0" r="6" fill="#c2d2ee">
        <animateTransform attributeName="transform" type="scale" begin="-0.125s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
    </circle>
    </g><g transform="translate(80 50)">
    <circle cx="0" cy="0" r="6" fill="#fefefe">
        <animateTransform attributeName="transform" type="scale" begin="0s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
    </circle>
    </g>
    </svg>`
    document.querySelector('.get-chart').style.display="None";
    console.log(StrForAuth)
    fetch('/prepare', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-Auth-Key': StrForAuth,
        'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value 
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        return response.json()
    })
    .then(chart => {
        console.log("am printing from index.js", chart)
        document.querySelector('.chart-content').innerHTML=`<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400"> ${ chart["diet-chart"] } <br><br>Do you like this Chart?</p>`
    })
}

