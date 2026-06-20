// Runs in the YouTube page's MAIN world so it can read the player response that
// the content script (isolated world) cannot see. It extracts the caption track
// list and posts it back to the content script via window.postMessage.
(function () {
  function findPlayerResponse() {
    try {
      if (window.ytInitialPlayerResponse) return window.ytInitialPlayerResponse;
    } catch (e) {}
    try {
      const args = window.ytplayer && window.ytplayer.config && window.ytplayer.config.args;
      const pr = args && (args.player_response || args.raw_player_response);
      if (typeof pr === "string") return JSON.parse(pr);
      if (pr) return pr;
    } catch (e) {}
    return null;
  }

  const pr = findPlayerResponse();
  let payload = { source: "tubescribe-inject", ok: false };

  if (pr) {
    const vd = pr.videoDetails || {};
    const tracks =
      (((pr.captions || {}).playerCaptionsTracklistRenderer || {}).captionTracks) || [];
    payload = {
      source: "tubescribe-inject",
      ok: true,
      videoId: vd.videoId || null,
      title: vd.title || null,
      tracks: tracks.map(function (t) {
        const name =
          (t.name && (t.name.simpleText ||
            (t.name.runs && t.name.runs.map(function (r) { return r.text; }).join("")))) ||
          t.languageCode;
        return {
          baseUrl: t.baseUrl,
          languageCode: t.languageCode,
          kind: t.kind || "",      // "asr" = auto-generated
          name: name
        };
      })
    };
  }

  window.postMessage(payload, "*");
})();
