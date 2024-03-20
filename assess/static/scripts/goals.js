
function addNewRecord(source) {
    console.warn('source: ', source);
    $('#editGoalModal').modal('show');
    $('#editGoalName').val('');
    $('#editGoalPriority').val('');
    $('#editGoalRollUp').val('');
    $('#editGoalType').val('');
    $('#action').val('add');
    $('#editGoalModalLabel').html('Add Goal');
    $('#btn-save').html('Add Goal');
    $('#btn-del').hide();
    if (source) {
        $('#editGoalType option').each(function() {
            if ($(this).val() === source) {
            $(this).prop('selected', true);
            }
        });
        $('#editGoalType').prop('disabled', true);   
    }
  }

  // Display the editGoalModal
  function openEditModal(goal_id, goal, rollUpGoal, priority, goal_type_id, action) {
    // var strRollUp = rollUpGoal.toString();
    clickedRow = $(this);
    console.warn('clickedRow: ', clickedRow);
    $('#editGoalModalLabel').html('Edit Goal');
    $('#btn-save').html('Save Changes');
    $('#btn-del').show();
    $('#editGoalName').val(goal);
    $('#goalId').val(goal_id);
    $('#editGoalPriority').val(priority);
    $('#action').val(action);
    $('#editGoalModal').modal('show');
    $('#editGoalRollUp option').each(function() {
      if ($(this).val() === rollUpGoal) {
        $(this).prop('selected', true);
      }
    });
    $('#editGoalType option').each(function() {
      if ($(this).val() === goal_type_id) {
        $(this).prop('selected', true);
      }
    });
    }

  function editGoal() {
    console.warn($('#editForm'));
    var myURL = "http://"+myapiserver+"/api/goaledit/";
    console.warn('myURL: ', myURL);
    $('#editGoalType').prop('disabled', false);   
    var formData = new FormData($('#editForm')[0]);
    var settings = {
    //   "url": "http://{{apiserver}}/api/goaledit/",
      "url": myURL,
      "method": "POST",
      "timeout": 0,
      "processData": false,
      "contentType": false,
      "data": formData,
    };
    console.warn('form Data: ', formData);

    $.ajax(settings).done(function (response) {
      console.log(response.message);
      let answer = response;
      console.error(answer);
      $("#addGoalModal").modal('hide');
      $("#editGoalModal").modal('hide');
      location.reload();
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.error('Error: ', errorThrown);
      console.error('Status: ', textStatus);
      console.error('jqXHR: ', jqXHR);
      alert('Error: ' + jqXHR.responseText);
    });

  };