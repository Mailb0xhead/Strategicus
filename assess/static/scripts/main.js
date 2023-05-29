function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
    }

    function toggleDisp(in_id,in_type) {

        var x = document.getElementById(in_id);
        console.log(x);
        if (x.style.display === "none") {
          x.style.display = in_type;
        } else {
          x.style.display = "none";
        }
        console.log("toggled");
      }
