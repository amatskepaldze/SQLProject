document.querySelector('.control').addEventListener('click', ()=>{
  document.querySelectorAll('.animation_blocks > span').forEach(el => el.classList.toggle("animation"))
});