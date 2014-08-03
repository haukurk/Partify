var gulp = require('gulp'),
    concat = require('gulp-concat');

var bower_src = { js: [], css: [], images: [], fonts: []};
function buildBowerSrc(packageLocation, list)
{
    list.push(packageLocation);
}

/* Bower Includes
*  Tip: USE minified versions - its not necessary to use uglify, css minify etc in this project. */
/* Bower - CSS */
buildBowerSrc('bower_components/bootstrap/dist/css/bootstrap.min.css',bower_src.css);
buildBowerSrc('bower_components/fontawesome/css/font-awesome.min.css',bower_src.css);
buildBowerSrc('bower_components/ionicons/css/ionicons.min.css',bower_src.css);
/* Bower - JS */
buildBowerSrc('bower_components/jquery/dist/jquery.min.js',bower_src.js);
buildBowerSrc('bower_components/bootstrap/dist/js/bootstrap.min.js',bower_src.js);

/* Bower - Fonts */
buildBowerSrc('bower_components/bootstrap/dist/fonts/*.{otf,eot,svg,ttf,woff}',bower_src.fonts);
buildBowerSrc('bower_components/ionicons/fonts/*.{otf,eot,svg,ttf,woff}',bower_src.fonts);
buildBowerSrc('bower_components/fontawesome/fonts/*.{otf,eot,svg,ttf,woff}',bower_src.fonts);

/* Build locations */
var build = {
    js: './partify/static/assets/js/',
	css: './partify/static/assets/css/',
	images: './partify/static/assets/images/',
	fonts: './partify/static/assets/fonts/'
};

gulp.task('build-bower-vendor-css', function() {
    return gulp.src(bower_src.css)
    .pipe(concat('vendor.css'))
    .pipe(gulp.dest(build.css));
});

gulp.task('build-bower-vendor-js', function() {
    return gulp.src(bower_src.js)
    .pipe(concat('vendor.js'))
    .pipe(gulp.dest(build.js));
});

gulp.task('build-bower-vendor-fonts', function() {
    return gulp.src(bower_src.fonts)
    .pipe(gulp.dest(build.fonts));
});

gulp.task('default', ['build-bower-vendor-css','build-bower-vendor-js','build-bower-vendor-fonts'], function() {

});