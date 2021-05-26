function setcookie(a,b,c) {if(c){var d = new Date();d.setDate(d.getDate()+c);}if(a && b) document.cookie = a+'='+b+(c ? '; expires='+d.toUTCString() : '');else return false;}
function getcookie(a) {var b = new RegExp(a+'=([^;]){1,}');var c = b.exec(document.cookie);if(c) c = c[0].split('=');else return false;return c[1] ? c[1] : false;}
function change(){
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
