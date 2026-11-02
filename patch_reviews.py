# -*- coding: utf-8 -*-
# Complete rewrite of the review interaction system
src = r'C:\Users\ijihu\Desktop\웹툰\index.html'

with open(src, 'r', encoding='utf-8') as f:
    code = f.read()

original_size = len(code)

# =====================================================================
# Find the full block from renderReviewsInContainer to openNicknameModal
# =====================================================================
start_marker = 'function renderReviewsInContainer(title, container, excludeMyOwn = false) {'
end_marker = 'function toggleDetailOtherReviews(title) {'

start_idx = code.find(start_marker)
end_idx = code.find(end_marker)

if start_idx < 0:
    print('ERROR: start_marker not found')
    exit(1)
if end_idx < 0:
    print('ERROR: end_marker not found')
    exit(1)

print(f'Replacing from char {start_idx} to {end_idx}')

NEW_BLOCK = r"""function renderReviewsInContainer(title, container, excludeMyOwn) {
  if (excludeMyOwn === undefined) excludeMyOwn = false;
  if (!container) return;
  const reviews = getReviewsForTitle(title, excludeMyOwn);
  if (!reviews.length) {
    container.innerHTML = '<div style="text-align:center;padding:18px;color:var(--text-muted);font-size:12px;">아직 다른 사용자가 남긴 감상평이 없습니다. 📝</div>';
    return;
  }
  const tKey = title.toLowerCase().replace(/\s+/g, '');
  const myId = currentUser ? currentUser.id : null;
  let html = '';
  reviews.forEach(function(r, idx) {
    const tierObj = TIERS.find(function(t){ return t.id === r.tier; });
    const sObj = STATUS[r.status];
    const isMe = myId && r.userId === myId;
    const addedStr = r.addedAt ? new Date(r.addedAt).toLocaleDateString('ko-KR') : '';
    const myReactionKey = myId ? (myId + '_on_' + r.userId) : '';
    const myReaction = myId && REACTION_DATA[tKey] ? (REACTION_DATA[tKey][myReactionKey] || {}) : {};
    const allR = REACTION_DATA[tKey] || {};
    let likeCount = 0, dislikeCount = 0;
    const suffix = '_on_' + r.userId;
    Object.keys(allR).forEach(function(k) {
      if (k.endsWith(suffix)) {
        if (allR[k].like) likeCount++;
        if (allR[k].dislike) dislikeCount++;
      }
    });
    const myLike = myReaction.like || false;
    const myDislike = myReaction.dislike || false;
    const comments = (COMMENTS_DATA[tKey] && COMMENTS_DATA[tKey][r.userId]) || [];
    const commentCount = comments.reduce(function(a,c){ return a + 1 + (c.replies ? c.replies.length : 0); }, 0);

    const btnLikeStyle = 'background:' + (myLike ? 'rgba(99,102,241,0.25)' : 'var(--bg-card)') + ';border:1px solid ' + (myLike ? '#6366f1' : 'var(--border-color)') + ';border-radius:8px;padding:3px 10px;font-size:12px;cursor:pointer;color:' + (myLike ? '#6366f1' : 'var(--text-muted)') + ';font-weight:700;';
    const btnDisStyle = 'background:' + (myDislike ? 'rgba(239,68,68,0.2)' : 'var(--bg-card)') + ';border:1px solid ' + (myDislike ? '#ef4444' : 'var(--border-color)') + ';border-radius:8px;padding:3px 10px;font-size:12px;cursor:pointer;color:' + (myDislike ? '#ef4444' : 'var(--text-muted)') + ';font-weight:700;';
    const cmtBoxId = 'cmts_' + idx + '_' + tKey;

    html += '<div style="background:var(--bg-hover);border:1px solid var(--border-color);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:8px;">';
    html += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">';
    html += '<div style="display:flex;align-items:center;gap:6px;">';
    html += '<span style="font-weight:800;font-size:12.5px;color:var(--text-main);">👤 ' + escapeHtml(r.author) + '</span>';
    if (r.authorTitle) html += '<span style="font-size:10px;background:rgba(99,102,241,0.15);color:#6366f1;font-weight:800;padding:1px 6px;border-radius:6px;">' + escapeHtml(r.authorTitle) + '</span>';
    if (isMe) html += '<span style="font-size:9.5px;background:rgba(16,185,129,0.15);color:#10b981;font-weight:800;padding:1px 5px;border-radius:4px;">나</span>';
    html += '</div>';
    html += '<div style="display:flex;align-items:center;gap:6px;">';
    if (tierObj) html += '<span class="ribbon ' + tierObj.cls + '" style="position:static;font-size:11px;padding:2px 7px;">' + tierObj.name + '</span>';
    if (r.rating > 0) html += '<span style="font-size:12px;font-weight:700;color:#f59e0b;">⭐ ' + r.rating + '점</span>';
    html += '</div></div>';
    html += '<div style="font-size:12.5px;line-height:1.6;color:var(--text-main);white-space:pre-wrap;background:var(--bg-card);padding:10px 12px;border-radius:8px;border:1px solid rgba(255,255,255,0.04);">' + escapeHtml(r.note) + '</div>';
    html += '<div style="display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--text-muted);">';
    html += '<span>' + (r.chapter ? '진행도: ' + escapeHtml(r.chapter) : (sObj ? sObj.emoji + ' ' + sObj.label : '')) + '</span>';
    html += '<span>' + addedStr + '</span></div>';
    html += '<div style="display:flex;align-items:center;gap:8px;margin-top:2px;">';
    html += '<button data-tkey="' + escapeHtml(tKey) + '" data-uid="' + escapeHtml(r.userId) + '" data-type="like" onclick="handleReactionClick(this)" style="' + btnLikeStyle + '">👍 ' + likeCount + '</button>';
    html += '<button data-tkey="' + escapeHtml(tKey) + '" data-uid="' + escapeHtml(r.userId) + '" data-type="dislike" onclick="handleReactionClick(this)" style="' + btnDisStyle + '">👎 ' + dislikeCount + '</button>';
    html += '<button data-cmtbox="' + cmtBoxId + '" onclick="handleToggleComments(this)" style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:8px;padding:3px 10px;font-size:12px;cursor:pointer;color:var(--text-muted);font-weight:700;">💬 ' + commentCount + '</button>';
    html += '</div>';
    html += '<div id="' + cmtBoxId + '" style="display:none;flex-direction:column;gap:6px;margin-top:4px;">';
    html += renderCommentsHtml(tKey, r.userId, idx, comments);
    html += '</div>';
    html += '</div>';
  });
  container.innerHTML = html;
  // Store current context for re-render
  container.dataset.reviewTitle = title;
  container.dataset.reviewExclude = excludeMyOwn ? '1' : '0';
}

function renderCommentsHtml(tKey, reviewUserId, reviewIdx, comments) {
  const myId = currentUser ? currentUser.id : null;
  let html = '';
  (comments || []).forEach(function(c, ci) {
    const isMyComment = myId && c.userId === myId;
    const dateStr = c.ts ? new Date(c.ts).toLocaleDateString('ko-KR') : '';
    html += '<div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:8px;padding:8px 10px;">';
    html += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">';
    html += '<span style="font-size:11.5px;font-weight:700;color:var(--text-main);">👤 ' + escapeHtml(getDisplayName(c.userId, c.author)) + '</span>';
    html += '<div style="display:flex;gap:6px;align-items:center;">';
    html += '<span style="font-size:10px;color:var(--text-muted);">' + dateStr + '</span>';
    if (isMyComment) html += '<button data-tkey="' + tKey + '" data-uid="' + reviewUserId + '" data-ci="' + ci + '" data-ri="null" onclick="handleDeleteComment(this)" style="background:none;border:none;color:#ef4444;font-size:11px;cursor:pointer;">삭제</button>';
    html += '</div></div>';
    html += '<div style="font-size:12px;color:var(--text-main);white-space:pre-wrap;">' + escapeHtml(c.text) + '</div>';
    html += '<div style="margin-top:6px;display:flex;flex-direction:column;gap:4px;padding-left:12px;border-left:2px solid var(--border-color);">';
    (c.replies || []).forEach(function(rep, ri) {
      const isMyReply = myId && rep.userId === myId;
      const repDate = rep.ts ? new Date(rep.ts).toLocaleDateString('ko-KR') : '';
      html += '<div style="display:flex;justify-content:space-between;align-items:flex-start;">';
      html += '<div><span style="font-size:11px;font-weight:700;color:#6366f1;">↩ ' + escapeHtml(getDisplayName(rep.userId, rep.author)) + '</span><span style="font-size:11px;color:var(--text-main);white-space:pre-wrap;display:block;margin-top:2px;">' + escapeHtml(rep.text) + '</span></div>';
      html += '<div style="display:flex;gap:4px;align-items:center;flex-shrink:0;">';
      html += '<span style="font-size:10px;color:var(--text-muted);">' + repDate + '</span>';
      if (isMyReply) html += '<button data-tkey="' + tKey + '" data-uid="' + reviewUserId + '" data-ci="' + ci + '" data-ri="' + ri + '" onclick="handleDeleteComment(this)" style="background:none;border:none;color:#ef4444;font-size:11px;cursor:pointer;">삭제</button>';
      html += '</div></div>';
    });
    html += '</div>';
    if (myId) {
      const replyBoxId = 'replybox_' + tKey + '_' + reviewUserId + '_' + ci;
      html += '<button onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display===\'none\'?\'flex\':\'none\'" style="margin-top:6px;background:none;border:none;font-size:11px;color:#6366f1;cursor:pointer;font-weight:700;">↩ 대댓글</button>';
      html += '<div id="' + replyBoxId + '" style="display:none;gap:6px;margin-top:4px;">';
      html += '<input placeholder="대댓글 입력..." style="flex:1;background:var(--bg-main);border:1px solid var(--border-color);border-radius:6px;padding:5px 8px;font-size:12px;color:var(--text-main);" id="repinp_' + tKey + '_' + reviewUserId + '_' + ci + '">';
      html += '<button data-tkey="' + tKey + '" data-uid="' + reviewUserId + '" data-ci="' + ci + '" onclick="handleSubmitReply(this)" style="background:#6366f1;border:none;border-radius:6px;padding:5px 10px;font-size:12px;color:#fff;cursor:pointer;font-weight:700;">등록</button>';
      html += '</div>';
    }
    html += '</div>';
  });
  if (myId) {
    html += '<div style="display:flex;gap:6px;margin-top:4px;">';
    html += '<input placeholder="댓글 입력..." style="flex:1;background:var(--bg-main);border:1px solid var(--border-color);border-radius:6px;padding:6px 10px;font-size:12px;color:var(--text-main);" id="cmtinp_' + tKey + '_' + reviewUserId + '">';
    html += '<button data-tkey="' + tKey + '" data-uid="' + reviewUserId + '" onclick="handleSubmitComment(this)" style="background:#6366f1;border:none;border-radius:6px;padding:6px 12px;font-size:12px;color:#fff;cursor:pointer;font-weight:700;">등록</button>';
    html += '</div>';
  } else {
    html += '<div style="font-size:11px;color:var(--text-muted);padding:4px 0;">댓글을 달려면 로그인하세요.</div>';
  }
  return html;
}

// data-attribute based handlers (no inline string args, no quote issues)
function handleReactionClick(btn) {
  const tKey = btn.dataset.tkey;
  const uid = btn.dataset.uid;
  const type = btn.dataset.type;
  toggleReaction(tKey, uid, type);
}

function handleToggleComments(btn) {
  const boxId = btn.dataset.cmtbox;
  const box = document.getElementById(boxId);
  if (!box) return;
  const isHidden = box.style.display === 'none' || !box.style.display;
  if (isHidden) {
    box.style.display = 'flex';
    box.style.flexDirection = 'column';
    box.style.gap = '6px';
  } else {
    box.style.display = 'none';
  }
}

function handleSubmitComment(btn) {
  if (!currentUser) { toast('로그인이 필요합니다.'); return; }
  const tKey = btn.dataset.tkey;
  const uid = btn.dataset.uid;
  submitComment(tKey, uid);
}

function handleSubmitReply(btn) {
  if (!currentUser) { toast('로그인이 필요합니다.'); return; }
  const tKey = btn.dataset.tkey;
  const uid = btn.dataset.uid;
  const ci = parseInt(btn.dataset.ci);
  submitReply(tKey, uid, ci);
}

function handleDeleteComment(btn) {
  if (!currentUser) return;
  const tKey = btn.dataset.tkey;
  const uid = btn.dataset.uid;
  const ci = parseInt(btn.dataset.ci);
  const ri = btn.dataset.ri === 'null' ? null : parseInt(btn.dataset.ri);
  deleteComment(tKey, uid, ci, ri);
}

function toggleComments(tKey, reviewUserId, btn) {
  // Legacy compat - find the cmtbox by data attribute
  if (btn && btn.dataset && btn.dataset.cmtbox) {
    handleToggleComments(btn);
  }
}

function showReplyInput(tKey, reviewUserId, ci, btn) {
  // Legacy compat
  const box = document.getElementById('replybox_' + tKey + '_' + reviewUserId + '_' + ci);
  if (!box) return;
  box.style.display = box.style.display === 'none' || !box.style.display ? 'flex' : 'none';
}

function submitComment(tKey, reviewUserId) {
  if (!currentUser) { toast('로그인이 필요합니다.'); return; }
  const inp = document.getElementById('cmtinp_' + tKey + '_' + reviewUserId);
  if (!inp || !inp.value.trim()) { toast('댓글을 입력하세요.'); return; }
  if (!COMMENTS_DATA[tKey]) COMMENTS_DATA[tKey] = {};
  if (!COMMENTS_DATA[tKey][reviewUserId]) COMMENTS_DATA[tKey][reviewUserId] = [];
  COMMENTS_DATA[tKey][reviewUserId].push({
    id: Date.now(),
    userId: currentUser.id,
    author: myNickname || currentUser.email,
    text: inp.value.trim(),
    ts: Date.now(),
    replies: []
  });
  inp.value = '';
  _persistReactionsComments();
}

function submitReply(tKey, reviewUserId, ci) {
  if (!currentUser) { toast('로그인이 필요합니다.'); return; }
  const inp = document.getElementById('repinp_' + tKey + '_' + reviewUserId + '_' + ci);
  if (!inp || !inp.value.trim()) { toast('대댓글을 입력하세요.'); return; }
  if (!COMMENTS_DATA[tKey]) COMMENTS_DATA[tKey] = {};
  if (!COMMENTS_DATA[tKey][reviewUserId]) COMMENTS_DATA[tKey][reviewUserId] = [];
  if (!COMMENTS_DATA[tKey][reviewUserId][ci]) return;
  if (!COMMENTS_DATA[tKey][reviewUserId][ci].replies) COMMENTS_DATA[tKey][reviewUserId][ci].replies = [];
  COMMENTS_DATA[tKey][reviewUserId][ci].replies.push({
    id: Date.now(),
    userId: currentUser.id,
    author: myNickname || currentUser.email,
    text: inp.value.trim(),
    ts: Date.now()
  });
  inp.value = '';
  _persistReactionsComments();
}

function deleteComment(tKey, reviewUserId, ci, ri) {
  if (!currentUser) return;
  if (!COMMENTS_DATA[tKey] || !COMMENTS_DATA[tKey][reviewUserId]) return;
  if (ri === null || ri === undefined) {
    const c = COMMENTS_DATA[tKey][reviewUserId][ci];
    if (!c || c.userId !== currentUser.id) { toast('본인 댓글만 삭제할 수 있습니다.'); return; }
    COMMENTS_DATA[tKey][reviewUserId].splice(ci, 1);
  } else {
    const replies = COMMENTS_DATA[tKey][reviewUserId][ci] && COMMENTS_DATA[tKey][reviewUserId][ci].replies;
    if (!replies || !replies[ri] || replies[ri].userId !== currentUser.id) { toast('본인 댓글만 삭제할 수 있습니다.'); return; }
    replies.splice(ri, 1);
  }
  _persistReactionsComments();
}

function toggleReaction(tKey, reviewUserId, type) {
  if (!currentUser) { toast('로그인이 필요합니다.'); return; }
  const myId = currentUser.id;
  const rKey = myId + '_on_' + reviewUserId;
  if (!REACTION_DATA[tKey]) REACTION_DATA[tKey] = {};
  if (!REACTION_DATA[tKey][rKey]) REACTION_DATA[tKey][rKey] = { like: false, dislike: false };
  const cur = REACTION_DATA[tKey][rKey];
  if (type === 'like') {
    cur.like = !cur.like;
    if (cur.like) cur.dislike = false;
  } else {
    cur.dislike = !cur.dislike;
    if (cur.dislike) cur.like = false;
  }
  _persistReactionsComments();
}

function _persistReactionsComments() {
  try {
    if (currentUser) {
      db._reactions = REACTION_DATA;
      db._comments = COMMENTS_DATA;
    }
    localStorage.setItem('wt_cached_reactions', JSON.stringify(REACTION_DATA));
    localStorage.setItem('wt_cached_comments', JSON.stringify(COMMENTS_DATA));
  } catch(e) {}
  if (currentUser) syncToCloud();
  // Re-render all open review containers
  document.querySelectorAll('[data-review-title]').forEach(function(container) {
    const title = container.dataset.reviewTitle;
    const exclude = container.dataset.reviewExclude === '1';
    if (title) renderReviewsInContainer(title, container, exclude);
  });
}

function openNicknameModal() {
  if (!currentUser) return;
  const cur = myNickname || '';
  const newName = prompt('표시될 닉네임을 입력하세요\n(비워두면 이메일 표시)', cur);
  if (newName === null) return;
  const trimmed = newName.trim();
  myNickname = trimmed;
  try { localStorage.setItem('wt_nickname_' + currentUser.id, trimmed); } catch(e) {}
  const el = document.getElementById('userEmailLabel');
  if (el) el.textContent = trimmed || currentUser.email;
  syncToCloudNow();
  toast('닉네임이 변경되었습니다: ' + (trimmed || currentUser.email));
}

"""

# Replace the block
new_code = code[:start_idx] + NEW_BLOCK + code[end_idx:]
print(f'Old size: {original_size}, New size: {len(new_code)}')

with open(src, 'w', encoding='utf-8') as f:
    f.write(new_code)

print('Saved!')
