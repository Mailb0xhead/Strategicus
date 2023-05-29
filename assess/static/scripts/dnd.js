document.addEventListener('DOMContentLoaded', (event) => {

    function handleDragStart(e) {
      this.style.opacity = '0.4';
      dragSrcEl = this;

      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/html', this.innerHTML);
    }

    function handleDragEnd(e) {
      this.style.opacity = '1';

      items.forEach(function (item) {
        item.classList.remove('over');
      });
    }

    function handleDragOver(e) {
      e.preventDefault();
      return false;
    }

    function handleDragEnter(e) {
      this.classList.add('over');
    }

    function handleDragLeave(e) {
      this.classList.remove('over');
    }
    function handleDrop(e) {
      e.stopPropagation(); // stops the browser from redirecting.
      if (dragSrcEl !== this) {
        dragSrcEl.innerHTML = this.innerHTML;
        this.innerHTML = e.dataTransfer.getData('text/html');
      }

      return false;
    }

    let items = document.querySelectorAll('.container .box');
    items.forEach(function(item) {
      item.addEventListener('dragstart', handleDragStart);
      item.addEventListener('dragover', handleDragOver);
      item.addEventListener('dragenter', handleDragEnter);
      item.addEventListener('dragleave', handleDragLeave);
      item.addEventListener('dragend', handleDragEnd);
      item.addEventListener('drop', handleDrop);
    });
    });

    // function allowDrop(ev) {
    //   ev.preventDefault();
    // }
    
    // function drag(ev) {
    //   ev.dataTransfer.setData("text", ev.target.id);
    // }
    
    // function drop(ev) {
    //   ev.preventDefault();
    //   var data = ev.dataTransfer.getData("text");
    //   ev.target.appendChild(document.getElementById(data));
    // }

    $(function() {
      var panelList = $();
      $('[id^="listId"]').each(function(){
          panelList = panelList.add(this);
      });
      console.log(panelList);
      panelList.sortable({
          update: function(event, ui) {
            var panelId = event.target.id;
            var imageIds = getIdsOfImages(panelId);
            console.log('Update triggered on ' + panelId + ' with image ids: ' + imageIds);
        }   //end update       
      });
  });

  function getIdsOfImages(panelId) {
      var values = [];
      $('#' + panelId + ' .listitem').each(function(index) {
        values.push($(this).attr("id").replace("itemNo", ""));
        var inputValue = $(this).find('input').val();
        console.log('inputvalue:  ',inputValue)
      });

      // $('#' + panelId + '.listitemClass').each(function(index) {
      //   values.push($(this).attr("id").replace("itemNo", ""));
      // });
      $('#outputvalues').val(values);
      return values;
  }

