function show_pass() {
	alert("hello");
	var show = document.getElementById("pass2");
	show.setAttribute('type','text');
	document.getElementById('showpass').style.display= "none";
	document.getElementById('hidepass').style.display= "block";
}