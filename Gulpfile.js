const gulp = require('gulp');
const livereload = require('gulp-livereload');
const sass = require('gulp-sass');
const rename = require('gulp-rename');
const babelify = require('babelify');
const browserify = require('browserify');
const source = require('vinyl-source-stream');
const watchify = require('watchify');

// Css
gulp.task('styles', () => sass_compile());

gulp.task('styles:live', () => sass_compile().pipe(livereload({ start: true })))

gulp.task('styles:watch', ['styles'], () => {
  return gulp.watch(['./static/css/*.scss', './static/css/*/*.scss'], ['styles:live'])
})

function sass_compile() {
  return gulp
    .src('static/css/index.scss')
    .pipe(sass())
    .pipe(rename('app.css'))
    .pipe(gulp.dest('static/css'));
}

// Javascript
gulp.task('build', () => { return compile() });
gulp.task('build:watch', () => { return compile(true) });

function compile(watch) {
  // var bundle_watch = watchify(browserify('./static/js/index.js'));
  var bundle = browserify('./static/js/index.js');

  function rebundle() {
    bundle
      .transform(babelify)
      .bundle()
      .on('error', (err) => { console.log(err); this.emit('end'); })
      .pipe(source('index.js'))
      .pipe(rename('app.js'))
      .pipe(gulp.dest('static/js'));
  }

  if (watch) {
    watchify(bundle).on('update', () => {
      console.log('--> Bundling...');
      rebundle();
    })
  }

  rebundle()
}

gulp.task('default', ['styles', 'build']);
gulp.task('watch', ['styles:watch', 'build:watch']);
