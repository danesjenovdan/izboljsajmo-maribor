document.addEventListener('DOMContentLoaded', function(event) {
  django.jQuery( document ).ready(function() {
    console.log('jquery ready');
    //django.jQuery('#initiative_statuses-4-group')
    django.jQuery('.reject').parent().parent().on('change', 'select[name$="0-reason_for_rejection"]', function() {
        console.log(this.value);
        var this_inline_idx = this.id[23]
        django.jQuery.get( "/v1/rejections/" + this.value, function( data ) {
            django.jQuery(`#id_initiative_statuses-${this_inline_idx}-0-email_content`).val(data.note)
        });
    });
  });
});

