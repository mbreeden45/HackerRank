// How one test case becomes a runnable program. Shared by the practice screen, the mock exam and tools/node_check.js,
// so the browser and the checks build test programs in exactly the same way.
//   preset problems: the test input IS the starting-data lines. It replaces the locked grey lines at the top, and nothing is typed.
//   stdin problems:  the locked parts stay as they are, and the test input is typed in.
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else { root.BP = root.BP || {}; root.BP.programs = api; }
})(typeof window !== 'undefined' ? window : this, function () {
  // The learner's own part of the editor text: everything between the locked top and the locked bottom.
  function openPart(P, editorCode) {
    let s = editorCode;
    if (P.prefix && s.startsWith(P.prefix)) s = s.slice(P.prefix.length);
    if (P.suffix && s.endsWith(P.suffix)) s = s.slice(0, s.length - P.suffix.length);
    return s;
  }
  function forTest(P, editorCode, input) {
    if (P.mode === 'preset') return { code: input + openPart(P, editorCode) + P.suffix, stdin: '' };
    return { code: editorCode, stdin: input };
  }
  return { openPart, forTest };
});
