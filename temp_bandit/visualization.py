@@ -5,91 +5,71 @@
 and rich-formatted output using the Rich library when available.
 """"""
 
-from typing import TYPE_CHECKING, List, Optional, Union, Any
+from typing import TYPE_CHECKING, List, Optional, Union, Any, Dict
 from pathlib import Path
 from kura.types import Cluster, ClusterTreeNode
 from kura.base_classes.visualization import BaseVisualizationModel
 
-RICH_AVAILABLE = False
+if TYPE_CHECKING:
+    from rich.console import Console
+    ConsoleType = Optional[""Console""]
+else:
+    ConsoleType = Any
 
 # Try to import Rich, fall back gracefully if not available
 try:
-    from rich.console import Console
-    from rich.tree import Tree
-    from rich.table import Table
-    from rich.panel import Panel
-    from rich.text import Text
-    from rich.align import Align
-    from rich.box import ROUNDED
-
+    import rich
+    import rich.console
+    import rich.tree
+    import rich.table
+    import rich.panel
+    import rich.text
+    import rich.align
+    import rich.box
     RICH_AVAILABLE = True
 except ImportError:
-    pass
-
-if TYPE_CHECKING:
-    from rich.console import Console
-    from rich.tree import Tree
-    from rich.table import Table
-    from rich.panel import Panel
-    from rich.text import Text
-    from rich.align import Align
-    from rich.box import Box
-    from rich.console import Console as ConsoleType
-else:
-    # These will only be used at runtime when Rich is not available
-    if not RICH_AVAILABLE:
-        # Define minimal classes for runtime use when Rich is not available
-        class Console:
-            def print(self, *args, **kwargs):
-                pass
+    class RichStub:
+        """"""Stub class for rich module when not available.""""""
         
-        class Tree:
-            def __init__(self, *args, **kwargs):
-                pass
-            
-            def add(self, *args, **kwargs):
-                return self
-        
-        class Table:
-            def __init__(self, *args, **kwargs):
-                pass
-            
-            def add_column(self, *args, **kwargs):
-                pass
-            
-            def add_row(self, *args, **kwargs):
-                pass
-        
-        class Panel:
-            def __init__(self, *args, **kwargs):
-                pass
+        class console:
+            """"""Stub for rich.console module.""""""
+            class Console:
+                """"""Stub for rich.console.Console class.""""""
+                def __init__(self, *args, **kwargs):
+                    pass
+                
+                def print(self, *args, **kwargs):
+                    print(*args)
         
-        class Text:
-            def __init__(self, *args, **kwargs):
-                pass
-        
-        class Align:
-            def __init__(self, *args, **kwargs):
-                pass
-        
-        class Box:
-            pass
-        
-        ROUNDED = Box()
+        class tree:
+            """"""Stub for rich.tree module.""""""
+            class Tree:
+                """"""Stub for rich.tree.Tree class.""""""
+                def __init__(self, *args, **kwargs):
+                    pass
+                
+                def add(self, *args, **kwargs):
+                    return self
     
-    ConsoleType = Any
+    rich = RichStub()
+    RICH_AVAILABLE = False
 
 
 class ClusterVisualizer(BaseVisualizationModel):
     """"""Handles visualization of hierarchical cluster structures.""""""
 
-    def __init__(self, console: Optional[""ConsoleType""] = None):
+    def __init__(self, console: Optional[ConsoleType] = None):
         """"""Initialize the visualizer.
 
         Args:
             console: Optional Rich Console instance for enhanced output
         """"""
-        self.console = console or (Console() if RICH_AVAILABLE else None)
+        if console is not None:
+            self.console = console
+        elif RICH_AVAILABLE:
+            self.console = rich.console.Console()
+        else:
+            self.console = None
     
     @property
     def checkpoint_filename(self) -> str:
@@ -121,7 +101,7 @@ def _load_clusters_from_checkpoint(self, checkpoint_path: Union[str, Path]) -> L
         except Exception as e:
             raise ValueError(f""Failed to load clusters from {checkpoint_path}: {e}"")
 
-    def _build_cluster_tree(self, clusters: List[Cluster]) -> dict[str, ClusterTreeNode]:
+    def _build_cluster_tree(self, clusters: List[Cluster]) -> Dict[str, ClusterTreeNode]:
         """"""Build a tree structure from a list of clusters.
 
         Args:
@@ -154,7 +134,7 @@ def visualize_clusters(
         *,
         checkpoint_path: Optional[Union[str, Path]] = None,
         style: str = ""basic"",
-        console: Optional[""ConsoleType""] = None,
+        console: Any = None,
     ) -> None:
         """"""Visualize a list of clusters.
         
@@ -178,227 +158,77 @@ def visualize_clusters(
             self.visualise_clusters_rich(clusters=clusters, checkpoint_path=checkpoint_path, console=output_console)
         else:
             raise ValueError(f""Invalid style '{style}'. Must be one of: basic, enhanced, rich"")
-
-    def _build_tree_structure(
-        self,
-        node: ClusterTreeNode,
-        node_id_to_cluster: dict[str, ClusterTreeNode],
-        level: int = 0,
-        is_last: bool = True,
-        prefix: str = """",
-    ) -> str:
-        """"""Build a text representation of the hierarchical cluster tree.
-
-        This is a recursive helper method used by visualise_clusters().
-
-        Args:
-            node: Current tree node
-            node_id_to_cluster: Dictionary mapping node IDs to nodes
-            level: Current depth in the tree (for indentation)
-            is_last: Whether this is the last child of its parent
-            prefix: Current line prefix for tree structure
-
-        Returns:
-            String representation of the tree structure
-        """"""
-        # Current line prefix (used for tree visualization symbols)
-        current_prefix = prefix
-
-        # Add the appropriate connector based on whether this is the last child
-        if level > 0:
-            if is_last:
-                current_prefix += ""╚══ ""
-            else:
-                current_prefix += ""╠══ ""
-
-        # Print the current node
-        result = (
-            current_prefix + node.name + "" ("" + str(node.count) + "" conversations)
""
-        )
-
-        # Calculate the prefix for children (continue vertical lines for non-last children)
-        child_prefix = prefix
-        if level > 0:
-            if is_last:
-                child_prefix += (
-                    ""    ""  # No vertical line needed for last child's children
-                )
-            else:
-                child_prefix += (
-                    ""║   ""  # Continue vertical line for non-last child's children
-                )
-
-        # Process children
-        children = node.children
-        for i, child_id in enumerate(children):
-            child = node_id_to_cluster[child_id]
-            is_last_child = i == len(children) - 1
-            result += self._build_tree_structure(
-                child, node_id_to_cluster, level + 1, is_last_child, child_prefix
-            )
-
-        return result
-
+            
     def visualise_clusters(
         self,
         clusters: Optional[List[Cluster]] = None,
         *,
         checkpoint_path: Optional[Union[str, Path]] = None,
     ) -> None:
         """"""Print a hierarchical visualization of clusters to the terminal.
-
-        This method builds a tree representation and prints it to the console.
-        The visualization shows the hierarchical relationship between clusters
-        with indentation and tree structure symbols.
-
+        
         Args:
             clusters: List of clusters to visualize. If None, loads from checkpoint_path
             checkpoint_path: Path to checkpoint file to load clusters from
-
+            
         Raises:
             ValueError: If neither clusters nor checkpoint_path is provided
             FileNotFoundError: If checkpoint file doesn't exist
-
-        Example output:
-        ╠══ Compare and improve Flutter and React state management (45 conversations)
-        ║   ╚══ Improve and compare Flutter and React state management (32 conversations)
-        ║       ╠══ Improve React TypeScript application (15 conversations)
-        ║       ╚══ Compare and select Flutter state management solutions (17 conversations)
-        ╠══ Optimize blog posts for SEO and improved user engagement (28 conversations)
         """"""
         if clusters is None:
             if checkpoint_path is None:
                 raise ValueError(""Either clusters or checkpoint_path must be provided"")
             clusters = self._load_clusters_from_checkpoint(checkpoint_path)
-
-        # Build tree structure
+            
         node_id_to_cluster = self._build_cluster_tree(clusters)
-
-        # Find root nodes and build the tree
-        root_nodes = [
-            node_id_to_cluster[cluster.id] for cluster in clusters if not cluster.parent_id
-        ]
-
-        total_conversations = sum(node.count for node in root_nodes)
-        fake_root = ClusterTreeNode(
-            id=""root"",
-            name=""Clusters"",
-            description=""All clusters"",
-            slug=""all_clusters"",
-            count=total_conversations,
-            children=[node.id for node in root_nodes],
-        )
-
-        tree_output = self._build_tree_structure(
-            fake_root, node_id_to_cluster, 0, False
-        )
-
-        print(tree_output)
-
-    def _build_enhanced_tree_structure(
+        
+        root_clusters = [cluster for cluster in clusters if not cluster.parent_id]
+        
+        for cluster in root_clusters:
+            node = node_id_to_cluster[cluster.id]
+            self._print_cluster_tree(node, node_id_to_cluster)
+            
+    def _print_cluster_tree(
         self,
         node: ClusterTreeNode,
-        node_id_to_cluster: dict[str, ClusterTreeNode],
+        node_id_to_cluster: Dict[str, ClusterTreeNode],
         level: int = 0,
         is_last: bool = True,
         prefix: str = """",
-        total_conversations: int = 0,
-    ) -> str:
-        """"""Build an enhanced text representation with colors and better formatting.
-
+    ) -> None:
+        """"""Print a text representation of the cluster tree.
+        
         Args:
             node: Current tree node
-            node_id_to_cluster: Dictionary mapping node IDs to nodes
-            level: Current depth in the tree (for indentation)
-            is_last: Whether this is the last child of its parent
-            prefix: Current line prefix for tree structure
-            total_conversations: Total conversations for percentage calculation
-
-        Returns:
-            String representation of the enhanced tree structure
+            node_id_to_cluster: Dictionary mapping node IDs to tree nodes
+            level: Current depth in the tree
+            is_last: Whether this is the last child at this level
+            prefix: Prefix string for indentation
         """"""
-        # Color scheme based on level
-        colors = [
-            ""bright_cyan"",
-            ""bright_green"",
-            ""bright_yellow"",
-            ""bright_magenta"",
-            ""bright_blue"",
-        ]
-        colors[level % len(colors)]
-
-        # Current line prefix (used for tree visualization symbols)
-        current_prefix = prefix
-
-        # Add the appropriate connector based on whether this is the last child
-        if level > 0:
-            if is_last:
-                current_prefix += ""╚══ ""
-            else:
-                current_prefix += ""╠══ ""
-
-        # Calculate percentage of total conversations
-        percentage = (
-            (node.count / total_conversations * 100) if total_conversations > 0 else 0
-        )
-
-        # Create progress bar for visual representation
-        bar_width = 20
-        filled_width = (
-            int((node.count / total_conversations) * bar_width)
-            if total_conversations > 0
-            else 0
-        )
-        progress_bar = ""█"" * filled_width + ""░"" * (bar_width - filled_width)
-
-        # Build the line with enhanced formatting
-        result = f""{current_prefix}🔸 {node.name}
""
-        result += f""{prefix}{'║   ' if not is_last and level > 0 else '    '}📊 {node.count:,} conversations ({percentage:.1f}%) [{progress_bar}]
""
-
-        # Add description if available and not too long
-        if (
-            hasattr(node, ""description"")
-            and node.description
-            and len(node.description) < 100
-        ):
-            result += f""{prefix}{'║   ' if not is_last and level > 0 else '    '}💭 {node.description}
""
-
-        result += ""
""
-
-        # Calculate the prefix for children
-        child_prefix = prefix
-        if level > 0:
-            if is_last:
-                child_prefix += ""    ""
-            else:
-                child_prefix += ""║   ""
-
-        # Process children
-        children = node.children
-        for i, child_id in enumerate(children):
-            child = node_id_to_cluster[child_id]
+        branch = ""└── "" if is_last else ""├── ""
+        
+        print(f""{prefix}{branch}{node.name} ({node.count} conversations)"")
+        
+        child_prefix = prefix + (""    "" if is_last else ""│   "")
+        
+        children = [node_id_to_cluster[child_id] for child_id in node.children]
+        for i, child in enumerate(children):
             is_last_child = i == len(children) - 1
-            result += self._build_enhanced_tree_structure(
-                child,
-                node_id_to_cluster,
-                level + 1,
-                is_last_child,
-                child_prefix,
-                total_conversations,
+            self._print_cluster_tree(
+                child, 
+                node_id_to_cluster, 
+                level + 1, 
+                is_last_child, 
+                child_prefix
             )
-
-        return result
-
+            
     def visualise_clusters_enhanced(
         self,
         clusters: Optional[List[Cluster]] = None,
         *,
         checkpoint_path: Optional[Union[str, Path]] = None,
     ) -> None:
-        """"""Print an enhanced hierarchical visualization of clusters with colors and statistics.
-
-        This method provides a more detailed visualization than visualise_clusters(),
-        including conversation counts, percentages, progress bars, and descriptions.
+        """"""Print an enhanced hierarchical visualization of clusters.
         
         Args:
             clusters: List of clusters to visualize. If None, loads from checkpoint_path
@@ -408,69 +238,52 @@ def visualise_clusters_enhanced(
             ValueError: If neither clusters nor checkpoint_path is provided
             FileNotFoundError: If checkpoint file doesn't exist
         """"""
-        print(""
"" + ""="" * 80)
-        print(""🎯 ENHANCED CLUSTER VISUALIZATION"")
-        print(""="" * 80)
-
         if clusters is None:
             if checkpoint_path is None:
                 raise ValueError(""Either clusters or checkpoint_path must be provided"")
             clusters = self._load_clusters_from_checkpoint(checkpoint_path)
-
-        # Build tree structure
+            
         node_id_to_cluster = self._build_cluster_tree(clusters)
-
-        # Calculate total conversations from root clusters only
+        
         root_clusters = [cluster for cluster in clusters if not cluster.parent_id]
+        
         total_conversations = sum(len(cluster.chat_ids) for cluster in root_clusters)
-
-        # Find root nodes
-        root_nodes = [node_id_to_cluster[cluster.id] for cluster in root_clusters]
-
-        fake_root = ClusterTreeNode(
-            id=""root"",
-            name=f""📚 All Clusters ({total_conversations:,} total conversations)"",
-            description=""Hierarchical conversation clustering results"",
-            slug=""all_clusters"",
-            count=total_conversations,
-            children=[node.id for node in root_nodes],
-        )
-
-        tree_output = self._build_enhanced_tree_structure(
-            fake_root, node_id_to_cluster, 0, False, """", total_conversations
-        )
-
-        print(tree_output)
-
-        # Add summary statistics
-        print(""="" * 80)
-        print(""📈 CLUSTER STATISTICS"")
-        print(""="" * 80)
-        print(f""📊 Total Clusters: {len(clusters)}"")
-        print(f""🌳 Root Clusters: {len(root_nodes)}"")
-        print(f""💬 Total Conversations: {total_conversations:,}"")
-        print(
-            f""📏 Average Conversations per Root Cluster: {total_conversations / len(root_nodes):.1f}""
-        )
-        print(""="" * 80 + ""
"")
-
+        
+        print(f""
📚 All Clusters ({total_conversations} conversations)
"")
+        
+        for cluster in sorted(root_clusters, key=lambda x: len(x.chat_ids), reverse=True):
+            node = node_id_to_cluster[cluster.id]
+            percentage = (node.count / total_conversations * 100) if total_conversations > 0 else 0
+            print(f""📊 {node.name} ({node.count} conversations, {percentage:.1f}%)"")
+            
+            if node.description:
+                print(f""   {node.description[:80]}..."" if len(node.description) > 80 else f""   {node.description}"")
+                
+            for child_id in node.children:
+                child = node_id_to_cluster[child_id]
+                child_percentage = (child.count / total_conversations * 100) if total_conversations > 0 else 0
+                print(f""  ├── 📌 {child.name} ({child.count} conversations, {child_percentage:.1f}%)"")
+                
+                for grandchild_id in child.children:
+                    grandchild = node_id_to_cluster[grandchild_id]
+                    grandchild_percentage = (grandchild.count / total_conversations * 100) if total_conversations > 0 else 0
+                    print(f""  │   └── 🔹 {grandchild.name} ({grandchild.count} conversations, {grandchild_percentage:.1f}%)"")
+            
+            print()  # Add spacing between root clusters
+            
     def visualise_clusters_rich(
         self,
         clusters: Optional[List[Cluster]] = None,
         *,
         checkpoint_path: Optional[Union[str, Path]] = None,
-        console: Optional[""ConsoleType""] = None,
+        console: Any = None,
     ) -> None:
         """"""Print a rich-formatted hierarchical visualization using Rich library.
-
-        This method provides the most visually appealing output with colors,
-        interactive-style formatting, and comprehensive statistics when Rich is available.
-        Falls back to enhanced visualization if Rich is not available.
         
         Args:
             clusters: List of clusters to visualize. If None, loads from checkpoint_path
             checkpoint_path: Path to checkpoint file to load clusters from
-            console: Rich Console instance for output. If None, uses instance console
+            console: Console instance for rich output. If None, uses instance console
             
         Raises:
             ValueError: If neither clusters nor checkpoint_path is provided
@@ -479,43 +292,32 @@ def visualise_clusters_rich(
         output_console = console or self.console
         
         if not RICH_AVAILABLE or not output_console:
-            print(
-                ""⚠️  Rich library not available or console disabled. Using enhanced visualization...""
-            )
+            print(""⚠️  Rich library not available or console disabled. Using enhanced visualization..."")
             self.visualise_clusters_enhanced(clusters, checkpoint_path=checkpoint_path)
             return
-
+            
         if clusters is None:
             if checkpoint_path is None:
                 raise ValueError(""Either clusters or checkpoint_path must be provided"")
             clusters = self._load_clusters_from_checkpoint(checkpoint_path)
-
-        # Build cluster tree structure
+            
         node_id_to_cluster = self._build_cluster_tree(clusters)
-
-        # Calculate total conversations from root clusters only
+        
         root_clusters = [cluster for cluster in clusters if not cluster.parent_id]
         total_conversations = sum(len(cluster.chat_ids) for cluster in root_clusters)
-
-        # Create Rich Tree
-        if Tree is None:
-            print(
-                ""⚠️  Rich Tree component not available. Using enhanced visualization...""
-            )
-            self.visualise_clusters_enhanced(clusters, checkpoint_path=checkpoint_path)
+        
+        if not RICH_AVAILABLE or not output_console:
             return
-
-        tree = Tree(
+            
+        tree = rich.tree.Tree(
             f""[bold bright_cyan]📚 All Clusters ({total_conversations:,} conversations)[/]"",
             style=""bold bright_cyan"",
         )
-
-        # Add root clusters to tree
+        
         root_nodes = [node_id_to_cluster[cluster.id] for cluster in root_clusters]
-
+        
         def add_node_to_tree(rich_tree, cluster_node, level=0):
             """"""Recursively add nodes to Rich tree with formatting.""""""
-            # Color scheme based on level
             colors = [
                 ""bright_green"",
                 ""bright_yellow"",
@@ -524,24 +326,13 @@ def add_node_to_tree(rich_tree, cluster_node, level=0):
                 ""bright_red"",
             ]
             color = colors[level % len(colors)]
-
-            # Calculate percentage
+            
             percentage = (
                 (cluster_node.count / total_conversations * 100)
                 if total_conversations > 0
                 else 0
             )
-
-            # Create progress bar representation
-            bar_width = 15
-            filled_width = (
-                int((cluster_node.count / total_conversations) * bar_width)
-                if total_conversations > 0
-                else 0
-            )
-            progress_bar = ""█"" * filled_width + ""░"" * (bar_width - filled_width)
-
-            # Create node label with rich formatting
+            
             label = f""[bold {color}]{cluster_node.name}[/] [dim]({cluster_node.count:,} conversations, {percentage:.1f}%)[/]""
             if hasattr(cluster_node, ""description"") and cluster_node.description:
                 short_desc = (
@@ -550,98 +341,18 @@ def add_node_to_tree(rich_tree, cluster_node, level=0):
                     else cluster_node.description
                 )
                 label += f""
[italic dim]{short_desc}[/]""
-            label += f""
[dim]Progress: [{progress_bar}][/]""
-
+                
             node = rich_tree.add(label)
-
-            # Add children
+            
             for child_id in cluster_node.children:
                 child = node_id_to_cluster[child_id]
                 add_node_to_tree(node, child, level + 1)
-
-        # Add all root nodes to the tree
+                
         for root_node in sorted(root_nodes, key=lambda x: x.count, reverse=True):
             add_node_to_tree(tree, root_node)
-
-        # Only create tables if Rich components are available
-        if Table is None or ROUNDED is None:
-            if output_console:
-                output_console.print(tree)
-            return
-
-        # Create statistics table
-        stats_table = Table(
-            title=""📈 Cluster Statistics"", box=ROUNDED, title_style=""bold bright_cyan""
-        )
-        stats_table.add_column(""Metric"", style=""bold bright_yellow"")
-        stats_table.add_column(""Value"", style=""bright_green"")
-
-        stats_table.add_row(""📊 Total Clusters"", f""{len(clusters):,}"")
-        stats_table.add_row(""🌳 Root Clusters"", f""{len(root_nodes):,}"")
-        stats_table.add_row(""💬 Total Conversations"", f""{total_conversations:,}"")
-        stats_table.add_row(
-            ""📏 Avg per Root Cluster"", f""{total_conversations / len(root_nodes):.1f}""
-        )
-
-        # Create cluster size distribution table
-        size_table = Table(
-            title=""📊 Cluster Size Distribution"",
-            box=ROUNDED,
-            title_style=""bold bright_magenta"",
-        )
-        size_table.add_column(""Size Range"", style=""bold bright_yellow"")
-        size_table.add_column(""Count"", style=""bright_green"")
-        size_table.add_column(""Percentage"", style=""bright_blue"")
-
-        # Calculate size distribution for root clusters
-        root_sizes = [node.count for node in root_nodes]
-        size_ranges = [
-            (""🔥 Large (>100)"", lambda x: x > 100),
-            (""📈 Medium (21-100)"", lambda x: 21 <= x <= 100),
-            (""📊 Small (6-20)"", lambda x: 6 <= x <= 20),
-            (""🔍 Tiny (1-5)"", lambda x: 1 <= x <= 5),
-        ]
-
-        for range_name, condition in size_ranges:
-            count = sum(1 for size in root_sizes if condition(size))
-            percentage = (count / len(root_sizes) * 100) if root_sizes else 0
-            size_table.add_row(range_name, f""{count}"", f""{percentage:.1f}%"")
-
-        # Display everything
-        if output_console:
-            output_console.print(""
"")
-
-            # Only use Panel and Align if they're available
-            if Panel is not None and Align is not None and Text is not None:
-                output_console.print(
-                    Panel(
-                        Align.center(
-                            Text(
-                                ""🎯 RICH CLUSTER VISUALIZATION"",
-                                style=""bold bright_cyan"",
-                            )
-                        ),
-                        box=ROUNDED,
-                        style=""bright_cyan"",
-                    )
-                )
-            else:
-                output_console.print(""[bold bright_cyan]🎯 RICH CLUSTER VISUALIZATION[/]"")
-
-            output_console.print(""
"")
-            output_console.print(tree)
-            output_console.print(""
"")
-
-            # Display tables side by side if Table.grid is available
-            if hasattr(Table, ""grid""):
-                layout = Table.grid(padding=2)
-                layout.add_column()
-                layout.add_column()
-                layout.add_row(stats_table, size_table)
-                output_console.print(layout)
-            else:
-                # Fallback to printing tables separately
-                output_console.print(stats_table)
-                output_console.print(size_table)
-
-            output_console.print(""
"")
+            
+        output_console.print(""
"")
+        output_console.print(""[bold bright_cyan]🎯 RICH CLUSTER VISUALIZATION[/]"")
+        output_console.print(""
"")
+        output_console.print(tree)
+        output_console.print(""
"")