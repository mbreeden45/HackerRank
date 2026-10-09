window.BP = window.BP || {};
BP.store = (function () {
  const KEY = 'builderPrep.v1';
  let data = null;
  function blank() { return { diagnostic: null, lessons: {}, problems: {}, quiz: {}, exams: [], cards: {}, theme: 'light' }; }
  function load() {
    try { data = JSON.parse(localStorage.getItem(KEY)) || blank(); } catch (e) { data = blank(); }
    return data;
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {} }
  return {
    get() { return data || load(); },
    update(fn) { fn(this.get()); save(); },
    problem(id) { const d = this.get(); return d.problems[id] || (d.problems[id] = { solved: false, attempts: 0, hints: 0, best: 0 }); },
    reset() { data = blank(); save(); },
  };
})();
