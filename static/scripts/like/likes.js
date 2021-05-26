function like(){
    if (a==1){
        for (let z=1;z<4;z++){
            let element = document.getElementById("i"+z);
            element.classList.remove("progress"+z);
            element.style.visibility='hidden';
        }
        document.cookie = 'animation=0; path=/';
        a = getcookie('animation');
    }else if (a==0){
        for (let z=1;z<4;z++){
            let element = document.getElementById("i"+z);
            element.classList.add("progress"+z);
            element.style.visibility='visible';
        }
        document.cookie = 'animation=1; path=/';
        a = getcookie('animation');
    }
}

let a = getcookie('animation');
if (a != 1){
    a = 1;
    change();
}
