document.addEventListener('DOMContentLoaded', function(event) {
  django.jQuery( document ).ready(function() {
    console.log('jquery ready');
    django.jQuery('#initiative_statuses-3-group').on('change', 'select[name="initiative_statuses-3-0-reason_for_rejection"]', function() {
        console.log(this.value);
        django.jQuery.get( "/v1/rejections/" + this.value, function( data ) {
            django.jQuery("#id_initiative_statuses-3-0-email_content").val(data.note)
        });
    });
  });
});
