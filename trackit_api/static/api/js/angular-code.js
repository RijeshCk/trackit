	var app = angular.module('AddtotrackApp',['ngCookies','infinite-scroll','ngRoute','ui.bootstrap']);
	app.config(function($routeProvider){$routeProvider
		.when('/ffHome',{
			template:'<h2>helloo</h2>'
		})
		.when('/forgot',{
			template:'<h1>sasas</h1>',
			controller:"forgot_account_controller"
		})
		.when('/reset',{
			template:'<h1>sasas</h1>',
			controller:"reset_account_controller"
		})
		.when('/verify/:key/',{controller:'verify_account_controller',
			template:'<h1>sasas</h1>'
	})
		
	});


	app.controller('forgot_account_controller',function($scope){
	console.log('here');
	$('#myModal').modal('show');
	});
	app.controller('verify_account_controller',function($scope,$route,$rootScope,$routeParams){
		console.log('in verify contoller');
		$('#myModal').modal('show');
		// console.log($routeParams.email);
		$scope.useremail = $routeParams.email;
		console.log($scope.useremail);
		$('#reset').show();
		console.log($scope.useremail);
	$rootScope.$on("CallParentMethod", function(){
           $scope.reset($scope.useremail);
        });

	});


	app.controller('reset_account_controller',function($scope,$routeParams,$route){
	
	console.log('here');
	$('#myModal').modal('show');
	});

	app.controller('Addtotrackcontroller',function($scope,$rootScope,$http,$timeout,$cookies,$window,$routeParams)
	{

		 $rootScope.$on("CallParentMethod", function(){
           $scope.reset(useremail);


        });
		 	$http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
			
			element = $window.document.getElementById('exampleInputemail1');
			base_url = $window.location.origin
			console.log(base_url);
			element.focus();
			
			$scope.AddtoTrack=function(){
				url1 = $scope.url;
				myregex = /[a-zA-Z]/;
				$http.get(base_url+'/product/?url='+url1).then(
					function sucessCallback()
					{
						$scope.url='';
						$scope.message= "Product has been added to our Tracking system";
						$scope.clickthis=true;
						$scope.checkErrors=true
						$scope.btnClass ='warning-true'
						$timeout(function checkErrors(){
							$scope.checkErrors=false
						},3600);
					}, 
					function errorCallback()
					{
						console.log(url1);
						if (!url1){
							$scope.message="Please provide url"
						}
						else{
							$scope.message='Sorry we could\'t process your request. Please check your url'}     
							$scope.checkErrors=true
							$scope.btnClass ='error-true'
							$timeout(function checkErrors(){
								$scope.checkErrors=false
							},3600);
							$scope.url = ''
							return false
						}
						);}
		password1 = $scope.password1;
		password2 = $scope.password2;
		console.log(password1,password2);


$scope.notifyme=function(product){
				console.log('test')
				$scope.product_name=product.name.name;
				$scope.id = product.name.id;
				$scope.price = parseInt(product.name.price);
				console.log($scope.price)
				$scope._price = 6;			
			}

$scope.ActivateNotification = function(id){
$scope._id=id;
console.log('here');
console.log('activate section'+$scope.drop_price);
$http({method:'POST',url:base_url+'/notify',data:{'id':$scope.id,'drop_price':$scope.drop_price,'pricedrop_email':$scope.pricedrop_email }}).then(
					function successsCallback(response,status)
					{console.log('Sucess ');},
					function errorCallback(response,status){
					console.log('failed');
					})
}

$scope.signup = function(){
	var csrf='{{ csrf_token }}';
	$http({method:'POST',url:base_url+'/signup/',data:{'username':$scope.username,'password':$scope.password1,'email':$scope.email},headers:{'X-CSRFToken':csrf}}).then(function successCallback(response,status)
	{
		$cookies["username"] = $scope.username;
		$window.location.href = base_url+'/Home'
		$scope.names = response.data.product_list;
		})
			var csrf ='{{csrf_token}}';
			password1 = $scope.password1;
			password2 = $scope.password2;

			}
			
			$scope.login=function(){
				console.log('test');
				var csrf=$cookies.csrftoken;
				$http({method:'POST',url:base_url+'/authenticate/',data:{'username':$scope.username,'password':$scope.password,'type':$scope.aana},headers: {'X-CSRFToken' : csrf }})
				.then(function successCallback(response,status){
					console.log("login successfully");
					$cookies["username"] = $scope.username;
					$scope.names = response.data.product_list;
					$window.location.reload();
				},
				function errorCallback(response,status){
					console.log(response.text)
					$scope.login_error_message='Invalid Credentials';
					$scope.login_error_class='login-error-true';
				}
				)
			}

			$scope.loggedin_user = $cookies["username"]
			if ($scope.loggedin_user){
				$scope.check_loggedin=$scope.loggedin_user;
				$scope.hehe='glyphicon glyphicon-user';
			}
			else{
				$scope.check_loggedin='Login/signup';
				$scope.hehe='glyphicon glyphicon-user'
				$scope.classlogout='hide-logout';
			}

			$scope.logout=function(){
				$('image-div').show()
				var csrf=$cookies.csrftoken;
				$http({method:'DELETE',url:base_url+'/authenticate', headers: {'X-CSRFToken' : csrf }}).then(
					function successCallback(response,status)
					{
						console.log("logout sucessfully in suceeeee");
						$cookies['username']='';
						$cookies.remove('username');

					},function errorCallback()
					{	
						$window.location.reload();					
						$cookies['username'] = '';
						$cookies.remove('username');
					});
				$cookies.remove('username');
			}
			$scope.reset = function(useremail){
				console.log('in reset fun'+$scope.useremail);
				var csrf=$cookies.csrftoken;
				console.log($scope.email);
				console.log($routeParams.type, $routeParams.id);
				$http({method:'POST',url:base_url+'/account/applyresetpassword/',data:{'password':$scope.password1,'email':$scope.useremail},
				headers: {'X-CSRFToken' : csrf }}).then(
				function sucessCallback(response,status){

					console.log("password reset successfully");
					console.log(response,status);
					$scope.confirmation_response_text =response.data['content']; 

				},
				function errorCallback(response,status){
					console.log('faild to reset password');
					$scope.confirmation_response_text =response.data['content']; 
				}


				)

			}

			// $scope.notifyme=function(name){
			// 	$scope.product_name = name;
			// 	// $http({method:'POST',url:base_url+'/notify',data:{'name':$scope.product_name}}).then(
			// 	// 	function successsCallback(response,status)
			// 	// 	{console.log('Sucess ');},
			// 	// 	function errorCallback(response,status){
			// 	// 		console.log('failed');
			// 	// 	}


			// 	// 	)

			// }

			$scope.resetpassword = function(){
				console.log('in reset fun');
				var csrf=$cookies.csrftoken;
				console.log($scope.email);
				$http({method:'POST',url:base_url+'/resetpassword/',data:{'email':$scope.email},
				headers: {'X-CSRFToken' : csrf }}).then(
				function sucessCallback(response,status){
					console.log("reset link sent to registerd email");
					console.log(response,status);
					$scope.confirmation_response_text =response.data['content']; 

				},
				function errorCallback(response,status){
					console.log('faild to send email');
					$scope.confirmation_response_text =response.data['content']; 
				}
				)
			}
			

			console.log("listing section");
			$http.get(base_url+"/fetchall/")
			.success(function(response,status)
				{ 
				$('#image-div').hide();
				$scope.names = response.product_list;
				console.log($scope.names);
			}
			).error($timeout(function(data, status, headers, config, statusText){
				if(status == 429)
				{
					$scope.error_message= "You have exceed daily Limit";
				}
				else if (status == 400)
				{
					$scope.error_message = "No products in tracklist"
				}
				$('#image-div').hide();
			},3));

	}); 
// angular.module('MyApp',['ngMaterial', 'ngMessages', 'material.svgAssetsCache'])
//   .config(function($mdIconProvider) {
//     $mdIconProvider
//       .iconSet('device', 'img/icons/sets/device-icons.svg', 24);
//   })
// .controller('AppCtrl', function($scope) {

//   $scope.color = {
//     red: Math.floor(Math.random() * 255),
//     green: Math.floor(Math.random() * 255),
//     blue: Math.floor(Math.random() * 255)
//   };

//   $scope.rating1 = 3;
//   $scope.rating2 = 2;
//   $scope.rating3 = 4;

//   $scope.disabled1 = Math.floor(Math.random() * 100);
//   $scope.disabled2 = 0;
//   $scope.disabled3 = 70;

//   $scope.invert = Math.floor(Math.random() * 100);

//   $scope.isDisabled = true;
// });
