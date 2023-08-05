(function () {
    var keyfileUrl = function (id, algo) {
        return girder.apiRoot + '/file/' + id + '/hashsum_file/' + algo;
    };

    girder.wrap(girder.views.FileInfoWidget, 'render', function (render) {
        render.call(this);

        this.$('.g-file-info-line[property="id"]').before(girder.templates.hashsum_download_fileInfo({
            file: this.model,
            keyfileUrl: keyfileUrl
        }));

        this.$('.g-keyfile-download').tooltip();

        return this;
    });
}());
