(function($){
  'use strict';

  $(document).ready(function() {
    $('.file').dblclick(function() {
      var $this = $(this);
      window.location.href = '/admin/assetmanager/file/select/' + $this.data('fileId') + '/?is_popup=1';
    });
  });
})(jet.jQuery);
