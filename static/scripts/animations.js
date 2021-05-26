let a=1;
function change(){
    if (a==1){
        for (let z=1;z<4;z++){
            let element = document.getElementById("i"+z);
            element.classList.remove("progress"+z);
            element.style.visibility='hidden';
        }
        let b = document.getElementById("button");
        a=0;
    }else if (a==0){
        for (let z=1;z<4;z++){
            let element = document.getElementById("i"+z);
            element.classList.add("progress"+z);
            element.style.visibility='visible';
        }
        let b = document.getElementById("button");
        a=1;
    }
}
