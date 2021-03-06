QUnit.test('options.title', function (assert) {
  var done = assert.async();
  var util = window.Util;
  var image = util.createImage();

  assert.expect(1);

  return new Viewer(image, {
    inline: true,

    built: function () {
      assert.notOk(util.hasClass(this.viewer.title, 'viewer-hide'));

      done();
    }
  });
});

QUnit.test('options.title: false', function (assert) {
  var done = assert.async();
  var util = window.Util;
  var image = util.createImage();

  assert.expect(1);

  return new Viewer(image, {
    inline: true,
    title: false,

    built: function () {
      assert.ok(util.hasClass(this.viewer.title, 'viewer-hide'));

      done();
    }
  });
});
