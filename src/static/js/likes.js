function likePost(post_id){
	$.get('/blog/like_post/', {post_id: post_id}, function(data){
		var desc = data == 1 ? " like" : " likes"; 

		$('#likes' + post_id).html(data + desc);
		$('#like-button' + post_id).hide();
	});
}