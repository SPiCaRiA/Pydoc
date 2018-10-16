#!/usr/bin/python
#-*- coding=utf-8 -*-

# file_detail_general = file_detail_class + file_detail_function_general + file_detail_function_details
# file_detail_class = file_detail_class_separate
#
# package_index_general = package_index_file_list
#
# package_main_general = package_main_files

file_detail_general = \
"""
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="../style.css">
	</head>
	<body>
		<div class="subTitle">$filename</div>
		<section class="contentContainer">
			<section class="summary">
				<ul class="blockList">
					<li class="blockList">
						<dl>
							<dt><span class="simpleTagLabel">$_file_annotation</span></dt>
                            <div class="block">$file_doc_text</div>
							%s
						</dl>
					</li>
				</ul>
		  </section>
		</section>

		<!-- iteration of class -->
		$class
		<!-- end of iteration of class -->

		<!-- function general -->
		$function_general
		<!-- end of function general -->

		<!-- function details -->
		$function_details
		<!-- end of function details -->
	</body>
</html>
"""

file_detail_function_general = \
"""
		<section class="contentContainer">
			<section class="summary">
				<ul class="blockList">
					<h3>$_function_general</h3>
					<li class="blockList">
						<table class="memberSummary" border="0" cellpadding="3" cellspacing="0" summary="$_function_general_table">
							<caption>
								<span class="tableTag">$_function</span>
							</caption>
							<tbody><tr>
								<th class="colFirst" scope="col">$_function</th>
								<th class="colLast" scope="col">$_param</th>
							</tr></tbody>
							%s
						</table>
					</li>
				</ul>
			</section>
		</section>
"""

file_detail_function_general_iter = \
"""
							<tbody>
								<!-- iteration of function -->
								<tr class="%s">
									<td class="colFirst">
										<a><code>$function%d_name</code></a>
									</td>
									<td class="colLast">$function%d_args</td>
								</tr>
								<!-- end iteration of function -->
							</tbody>
"""

file_detail_function_details = \
"""
		<section class="contentContainer">
			<section class="summary">
				<ul class="blockList">
					<h3>$_function_details</h3>
					%s
				</ul>
			</section>
		</section>
"""

file_detail_function_details_iter = \
"""
					<!-- iteration of function details -->
					<li class="blockList">
						<h4>$function%d_name</h4>
						<pre>$function%d_name($function%d_args)</pre>
						<div class="block">
						$function%d_doc_text
						</div>

						<!-- iteration of comments -->
						<dl>
							%s
						</dl>
						<!-- end of iteration of comments -->
					</li>
					<!-- end of iteration of function details -->
"""

file_detail_class = \
"""
		<section class="classInFile">
		<section class="header">
			<h2 class="title">$_class $class_name</h2>
		</section>

		<section class="contentContainer">
			<ul class="inheritance">
				$super
			</ul>

			<ul class="blockList">
				$class_comment
			</ul>

			<section class="summary">
				<ul class="blockList">
					$method_general
				</ul>
			</section>

			<section class="summary">
				<ul class="blockList">
					$cons_general
				</ul>
			</section>

			<section class="summary">
				<ul class="blockList">
					$cons_details
				</ul>
			</section>

			<!-- methods details -->
			<section class="summary">
				<ul class="blockList">
					$method_details
				</ul>
			</section>
	    </section>
	  </section>
"""

# separate

file_detail_class_super = \
"""
				<!-- super -->
					%s
				<!-- end super -->
"""

file_detail_class_super_iter = \
"""
					<!-- iteration of super classes -->
					<li>$super%d</li>
					<!-- end iteration-->
"""


file_detail_class_info = \
"""
				<!-- $class_info -->
				<li class="blockList">
						<div class="block classDoc">$class_doc_text</div>
						<dl>
							%s
						</dl>
					</li>
				<!-- end $class_info -->
"""

file_detail_class_method_general = \
"""
				<!-- method_general -->
					<h3>$_method_general</h3>
					<li class="blockList">
						<table class="memberSummary" border="0" cellpadding="3" cellspacing="0" summary="$_method_general_table">
							<caption>
								<span class="tableTag">$_method</span>
							</caption>
							<tbody><tr>
								<th class="colFirst" scope="col">$_method</th>
								<th class="colLast" scope="col">$_param</th>
							</tr></tbody>

							<tbody>
								%s
							</tbody>
						</table>
					</li>
				<!-- end method_general -->
"""

file_detail_class_method_general_iter = \
"""
								<!-- iteration of methods -->
								<tr class="%s">
									<td class="colFirst">
										<a><code>$method%d_name</code></a>
									</td>
									<td class="colLast">$method%d_args</td>
								</tr>
								<!-- end of iteration -->
"""

file_detail_class_cons_general = \
"""
				<!-- cons_general -->
					<h3>$_cons_general</h3>
					<li class="blockList">
						<table class="memberSummary" border="0" cellpadding="3" cellspacing="0" summary="$_cons_general_table">
							<caption>
								<span class="tableTag">$_cons</span>
							</caption>
							<tbody><tr>
								<th class="colLast" scope="col">__init__</th>
							</tr></tbody>

							<tbody>
								<tr class="altColor">
									<td class="colFirst">
										<a><code>__init__($cons_args)</code></a>
									</td>
								</tr>
							</tbody>
						</table>
					</li>
				<!-- end cons_general -->
"""

file_detail_class_cons_details = \
"""
				<!-- cons_details -->
					<h3>$_cons_details</h3>
					<li class="blockList">
						<h4>__init__</h4>
						<pre>__init__($cons_args)</pre>
						<div class="block">
						$cons_doc_text
						</div>
						<dl>
							%s
						</dl>
					</li>
				<!-- end cons_details -->
"""

file_detail_class_method_details = \
"""
				<!-- method_details -->
					<h3>$_method_details</h3>
					<li class="blockList">
						%s
					</li>
				<!-- end method_details -->
"""

file_detail_class_method_details_iter = \
"""
						<!-- method iteration -->
						<h4>$method%d_name</h4>
						<pre>$method%d_name($method%d_args)</pre>
						<div class="block">
						$method%d_doc_text
						</div>
						<dl>
                            %s
						</dl>
						<!-- end method iteraion -->
"""

package_index_general = \
"""
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<!-- sidebar -->
		<section class="sidebar" id="sidebar">
			<h1 class="bar">$_all_files</h1>
			<section class="indexContainer">
				<ul>
					$file_list
				</ul>
			</section>
		</section>
		<!-- end sidebar -->

		<!-- mainframe -->
		<section>
			<iframe src="index_main.html" class="main_frame"></iframe>
		</section>
		<!-- end mainframe -->
	</body>
</html>
"""

package_index_file_list = \
"""
				<!-- iteration of file list -->
				<li>
					<a href="%s" target="classFrame">%s</a>
				</li>
				<!-- end iteration of file list -->
"""

package_index_main_general = \
"""
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<section>
				<h1 class="title">$_package</h1>
				<table class="typeSummary" border="0" cellpadding="3" cellspacing="0">
					<caption>
						<span class="tableTag">$_file</span>
					</caption>

					<tbody>
						<tr>
							<th class="colFirst" scope="col">$_file</th>
							<th class="colLast" scope="col">$_demostration</th>
						</tr>
					</tbody>

					<tbody>
						$files
					</tbody>
				</table>
			</section>
    </body>
</html>
"""

package_index_main_files = \
"""
					<tr class="%s">
						<td class="colFirst">
							<a href="%s">%s</a>
						</td>
						<td class="colLast">
							<div class="block">%s</div>
						</td>
					</tr>
"""

comment_string = {
    "version": """<dt><span class="simpleTagLabel">$_version</span></dt>
<dd>$%s</dd>""",
    "author": """<dt><span class="simpleTagLabel">$_author</span></dt>
<dd>$%s</dd>""",
    "since": """<dt><span class="simpleTagLabel">$_since</span></dt>
<dd>$%s</dd>""",

    "param": """<dt><span class="simpleTagLabel">$_param</span></dt>
<dd>$%s</dd>""",
    "return": """<dt><span class="simpleTagLabel">$_return</span></dt>
<dd>$%s</dd>""",
    "throws": """<dt><span class="simpleTagLabel">$_throws</span></dt>
<dd>$%s</dd>""",
}
